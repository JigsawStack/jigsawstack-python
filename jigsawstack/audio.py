import json
import re
import struct
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Union,
    cast,
    overload,
)

try:
    from silero_vad_lite import SileroVAD as _SileroVAD

    _HAS_SILERO = True
except ImportError:
    _HAS_SILERO = False

try:
    import audioop as _audioop
except (ImportError, ModuleNotFoundError):
    _audioop = None  # type: ignore[assignment]

import aiohttp
from typing_extensions import Literal, NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest, AsyncRequestConfig
from .exceptions import raise_for_code_and_type
from .request import Request, RequestConfig


def _pcm_to_wav_bytes(
    pcm_bytes: bytes, sample_rate: int, channels: int, sample_width: int
) -> bytes:
    data_size = len(pcm_bytes)
    bits_per_sample = sample_width * 8
    byte_rate = sample_rate * channels * sample_width
    block_align = channels * sample_width
    riff_chunk_size = 36 + data_size

    header = (
        b"RIFF"
        + riff_chunk_size.to_bytes(4, "little")
        + b"WAVE"
        + b"fmt "
        + (16).to_bytes(4, "little")
        + (1).to_bytes(2, "little")  # PCM format
        + channels.to_bytes(2, "little")
        + sample_rate.to_bytes(4, "little")
        + byte_rate.to_bytes(4, "little")
        + block_align.to_bytes(2, "little")
        + bits_per_sample.to_bytes(2, "little")
        + b"data"
        + data_size.to_bytes(4, "little")
    )

    return header + pcm_bytes


def _tokenize_text(text: str) -> List[str]:
    return [token for token in text.strip().split() if token]


def _join_tokens(tokens: List[str]) -> str:
    return " ".join(tokens).strip()


def _is_meaningful_token(token: str) -> bool:
    return any(char.isalnum() for char in token)


def _normalize_token(token: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", token.lower())


# Known Whisper hallucination phrases that appear at the end of short audio clips.
_WHISPER_HALLUCINATIONS = [
    "thank you",
    "thanks for watching",
    "thanks for listening",
    "subscribe",
    "please subscribe",
    "like and subscribe",
    "see you next time",
    "bye",
    "goodbye",
    "the end",
]


def _strip_trailing_hallucination(text: str) -> str:
    """Remove known Whisper hallucination phrases from the end of a transcript."""
    stripped = text.rstrip(". !?,")
    lower = stripped.lower()
    for phrase in _WHISPER_HALLUCINATIONS:
        if lower.endswith(phrase):
            trimmed = stripped[: -len(phrase)].rstrip(" .,!?")
            if trimmed:
                return trimmed
    return text


def _fuzzy_token_match(a: str, b: str) -> bool:
    """Check if two tokens match, allowing for minor ASR differences."""
    na, nb = _normalize_token(a), _normalize_token(b)
    if na == nb:
        return True
    # Allow 1 character edit distance for tokens >= 4 chars
    if len(na) >= 4 and len(nb) >= 4:
        if abs(len(na) - len(nb)) <= 1:
            # Simple Levenshtein check for distance <= 1
            if len(na) == len(nb):
                return sum(c1 != c2 for c1, c2 in zip(na, nb)) <= 1
            # Handle insertion/deletion
            short, long = (na, nb) if len(na) < len(nb) else (nb, na)
            diffs = 0
            si = li = 0
            while si < len(short) and li < len(long):
                if short[si] != long[li]:
                    diffs += 1
                    li += 1
                else:
                    si += 1
                    li += 1
            return diffs + (len(long) - li) <= 1
    return False


def _find_token_overlap(previous: List[str], current: List[str]) -> int:
    max_overlap = min(len(previous), len(current))
    for overlap in range(max_overlap, 0, -1):
        previous_slice = previous[-overlap:]
        current_slice = current[:overlap]
        if all(
            _fuzzy_token_match(previous_slice[i], current_slice[i])
            for i in range(overlap)
        ):
            return overlap
    return 0


def _tokens_match(left: List[str], right: List[str]) -> bool:
    if len(left) != len(right):
        return False
    return all(
        _normalize_token(left[i]) == _normalize_token(right[i])
        for i in range(len(left))
    )


def _merge_incremental_text(
    chunk_text: str,
    previous_tokens: List[str],
    committed_tokens: List[str],
    pending_tokens: List[str],
    pending_hits: int,
    stability_rounds: int,
    force_commit: bool = False,
) -> tuple[List[str], List[str], List[str], int, str]:
    current_tokens = _tokenize_text(chunk_text)
    delta_text = ""

    if not current_tokens:
        if force_commit and pending_tokens:
            overlap_committed = _find_token_overlap(committed_tokens, pending_tokens)
            to_commit = [
                token
                for token in pending_tokens[overlap_committed:]
                if _is_meaningful_token(token)
            ]
            if to_commit:
                committed_tokens.extend(to_commit)
                delta_text = _join_tokens(to_commit)
            pending_tokens = []
            pending_hits = 0
        return previous_tokens, committed_tokens, pending_tokens, pending_hits, delta_text

    overlap_previous = _find_token_overlap(previous_tokens, current_tokens)
    new_tokens = current_tokens[overlap_previous:]

    if new_tokens:
        if _tokens_match(pending_tokens, new_tokens):
            pending_hits += 1
        else:
            pending_tokens = new_tokens
            pending_hits = 1
    elif pending_tokens and current_tokens and _tokens_match(pending_tokens, current_tokens):
        # Same text repeated with full overlap — count as stability confirmation
        pending_hits += 1
    else:
        pending_tokens = []
        pending_hits = 0

    should_commit = (
        bool(pending_tokens)
        and (pending_hits >= max(1, stability_rounds) or force_commit)
    )
    if should_commit:
        overlap_committed = _find_token_overlap(committed_tokens, pending_tokens)
        to_commit = [
            token
            for token in pending_tokens[overlap_committed:]
            if _is_meaningful_token(token)
        ]
        if to_commit:
            committed_tokens.extend(to_commit)
            delta_text = _join_tokens(to_commit)
        pending_tokens = []
        pending_hits = 0

    return current_tokens, committed_tokens, pending_tokens, pending_hits, delta_text


def _tail_text_from_segments(
    segments: List[Dict[str, Any]], cutoff_seconds: float
) -> str:
    tail_parts: List[str] = []
    for segment in segments:
        text = segment.get("text")
        timestamp = segment.get("timestamp")
        if not isinstance(text, str) or not text.strip():
            continue
        if (
            isinstance(timestamp, (list, tuple))
            and len(timestamp) == 2
            and all(isinstance(v, (int, float)) for v in timestamp)
        ):
            end = float(timestamp[1])
            if end >= cutoff_seconds:
                tail_parts.append(text.strip())

    return " ".join(tail_parts).strip()


class SpeechToTextParams(TypedDict):
    url: NotRequired[str]
    """
    the url of the audio file to transcribe, optional if file_store_key is provided
    """

    file_store_key: NotRequired[str]
    """
    the file store key of the audio file to transcribe, optional if url is provided
    """

    language: NotRequired[Union[str, Literal["auto"]]]
    """
    The language to transcribe or translate the file into. Use “auto” for automatic language detection, or specify a language code. If not specified, defaults to automatic detection. All supported language codes can be found
    """

    translate: NotRequired[bool]
    """
    When set to true, translates the content into English (or the specified language if language parameter is provided)
    """

    by_speaker: NotRequired[bool]
    """
    Identifies and separates different speakers in the audio file. When enabled, the response will include a speakers array with speaker-segmented transcripts.
    """

    webhook_url: NotRequired[str]
    """
    Webhook URL to send result to. When provided, the API will process asynchronously and send results to this URL when completed.
    """

    batch_size: NotRequired[int]
    """
    The batch size to return. Maximum value is 40. This controls how the audio is chunked for processing.
    """

    chunk_duration: NotRequired[int]
    """
    the duration of each chunk in seconds, maximum value is 15, defaults to 3
    """

    stream: NotRequired[bool]
    """
    Enable streaming response mode.
    """


class LiveSpeechToTextOptions(SpeechToTextParams, total=False):
    incremental: bool
    """
    Enable SDK-side incremental sliding-window transcription. Defaults to False.
    """

    window_seconds: float
    """
    Sliding window size in seconds for incremental mode. Defaults to 3.0.
    """

    hop_seconds: float
    """
    Hop interval in seconds between incremental requests. Defaults to 0.8.
    """

    stability_rounds: int
    """
    Number of consecutive windows required before committing new words. Defaults to 2.
    """

    emit_raw_events: bool
    """
    In incremental mode, forward raw SSE events from each window request. Defaults to False.
    """

    tail_context_seconds: float
    """
    Extra context kept before the tail cutoff when extracting new text from window segments. Defaults to 0.25.
    """

    max_chunk_seconds: float
    """
    Maximum buffered audio duration before forcing a flush. Defaults to 3.0 seconds.
    """

    min_chunk_seconds: float
    """
    Minimum buffered audio duration before allowing silence-triggered flush. Defaults to 0.25 seconds.
    """

    sample_rate: int
    """
    PCM sample rate in Hz. Defaults to 16000.
    """

    channels: int
    """
    Number of PCM channels. Defaults to 1.
    """

    sample_width: int
    """
    PCM sample width in bytes. Defaults to 2 (16-bit PCM).
    """

    speech_threshold: float
    """
    Speech probability threshold for VAD (0.0-1.0). Defaults to 0.5.
    When silero-vad-lite is installed, this is the Silero VAD probability threshold.
    Otherwise falls back to audioop RMS with a default threshold of 80.
    """

    silence_flush_seconds: float
    """
    Silence duration required after speech to flush early. Defaults to 0.45 seconds.
    """


class ChunkParams(TypedDict):
    text: str
    timestamp: tuple[int, int]


class BySpeakerParams(ChunkParams):
    speaker: str
    timestamp: tuple[int, int]
    text: str


class SpeechToTextResponse(BaseResponse):
    text: str
    """
    the text of the transcription
    """

    chunks: List[ChunkParams]
    """
    the chunks of the transcription
    """

    speakers: Optional[List[BySpeakerParams]]
    """
    the speakers of the transcription, available if by_speaker is set to true
    """

    language_detected: Optional[Dict[str, Any]]
    """
    the language detected in the transcription, available if language is set to auto
    """


class SpeechToTextWebhookResponse(BaseResponse):
    status: Literal["processing", "error"]
    """
    the status of the transcription process
    """

    id: str
    """
    the id of the transcription process
    """


class Audio(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(base_url=base_url, api_key=api_key, headers=headers)

    @overload
    def speech_to_text(
        self, params: SpeechToTextParams
    ) -> Union[SpeechToTextResponse, SpeechToTextWebhookResponse]: ...
    @overload
    def speech_to_text(
        self, blob: bytes, options: Optional[SpeechToTextParams] = None
    ) -> Union[SpeechToTextResponse, SpeechToTextWebhookResponse]: ...

    def speech_to_text(
        self,
        blob: Union[SpeechToTextParams, bytes],
        options: Optional[SpeechToTextParams] = None,
    ) -> Union[SpeechToTextResponse, SpeechToTextWebhookResponse]:
        options = options or {}
        path = "/ai/transcribe"
        if isinstance(blob, dict):
            # URL or file_store_key based request
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = Request(
            config=self.config,
            path=path,
            params=options,
            verb="post",
            files=files,
        ).perform_with_content()
        return resp

    @overload
    def speech_to_text_stream(
        self, params: SpeechToTextParams
    ) -> Generator[Union[Dict[str, Any], str], None, None]: ...

    @overload
    def speech_to_text_stream(
        self, blob: bytes, options: Optional[SpeechToTextParams] = None
    ) -> Generator[Union[Dict[str, Any], str], None, None]: ...

    def speech_to_text_stream(
        self,
        blob: Union[SpeechToTextParams, bytes],
        options: Optional[SpeechToTextParams] = None,
    ) -> Generator[Union[Dict[str, Any], str], None, None]:
        """
        Stream speech-to-text events from JigsawStack using SSE (`stream=true`).
        """
        options = options or {}
        path = "/ai/transcribe"

        if isinstance(blob, dict):
            params = dict(cast(Dict[str, Any], blob))
            params["stream"] = True
            req = Request(
                config=self.config,
                path=path,
                params=params,
                verb="post",
                stream=True,
            )
        else:
            params = dict(cast(Dict[str, Any], options))
            params["stream"] = True
            params["by_speaker"] = False
            if not params.get("language") or params.get("language") == "auto":
                params["language"] = "en"
            params.pop("webhook_url", None)

            files = {"file": blob}
            req = Request(
                config=self.config,
                path=path,
                params=params,
                verb="post",
                files=files,
                stream=True,
            )

        resp = req.make_request(url=f"{self.config['base_url']}{path}")
        self._raise_if_stream_error(resp)

        return self._iter_sse_events(resp)

    def live_speech_to_text(
        self,
        audio_stream: Iterable[bytes],
        options: Optional[LiveSpeechToTextOptions] = None,
    ) -> Generator[Union[Dict[str, Any], str], None, None]:
        """
        Stateless live transcription helper.

        Algorithm:
        - Accumulate audio up to 3 seconds (configurable)
        - Flush earlier when speech was detected and then silence persists
        - Send each flushed chunk to `/ai/transcribe` with `stream=true`
        - Yield SSE events from each chunk request

        The `audio_stream` must yield PCM frames (default: 16kHz, mono, 16-bit).
        """
        opts = dict(cast(Dict[str, Any], options or {}))

        incremental = bool(opts.pop("incremental", False))
        window_seconds = float(opts.pop("window_seconds", 3.0))
        hop_seconds = float(opts.pop("hop_seconds", 0.8))
        stability_rounds = int(opts.pop("stability_rounds", 2))
        emit_raw_events = bool(opts.pop("emit_raw_events", False))
        tail_context_seconds = float(opts.pop("tail_context_seconds", 0.25))
        max_chunk_seconds = float(opts.pop("max_chunk_seconds", 3.0))
        min_chunk_seconds = float(opts.pop("min_chunk_seconds", 0.25))
        sample_rate = int(opts.pop("sample_rate", 16000))
        channels = int(opts.pop("channels", 1))
        sample_width = int(opts.pop("sample_width", 2))
        speech_threshold = float(opts.pop("speech_threshold", 0.5))
        opts.pop("silence_rms_threshold", None)
        silence_flush_seconds = float(opts.pop("silence_flush_seconds", 0.45))

        if max_chunk_seconds <= 0:
            raise ValueError("max_chunk_seconds must be > 0")
        if min_chunk_seconds < 0:
            raise ValueError("min_chunk_seconds must be >= 0")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        if hop_seconds <= 0:
            raise ValueError("hop_seconds must be > 0")
        if stability_rounds <= 0:
            raise ValueError("stability_rounds must be > 0")
        if tail_context_seconds < 0:
            raise ValueError("tail_context_seconds must be >= 0")
        if sample_rate <= 0:
            raise ValueError("sample_rate must be > 0")
        if channels <= 0:
            raise ValueError("channels must be > 0")
        if sample_width not in (1, 2, 4):
            raise ValueError("sample_width must be 1, 2, or 4 bytes")

        bytes_per_second = sample_rate * channels * sample_width

        request_options = cast(SpeechToTextParams, opts)
        request_options["stream"] = True
        request_options["by_speaker"] = False
        if not request_options.get("language") or request_options.get("language") == "auto":
            request_options["language"] = "en"
        request_options.pop("webhook_url", None)

        def frame_duration_seconds(frame: bytes) -> float:
            return len(frame) / bytes_per_second

        # --- VAD setup ---
        _vad_leftover_samples_sync: list = []
        if _HAS_SILERO:
            _vad_model_sync = _SileroVAD(sample_rate)
            _SILERO_FRAMES = 512

            def has_speech(frame: bytes) -> bool:
                if not frame:
                    return False
                n_samples = len(frame) // 2
                samples = struct.unpack(f"<{n_samples}h", frame[: n_samples * 2])
                all_samples = _vad_leftover_samples_sync + list(samples)
                _vad_leftover_samples_sync.clear()
                detected = False
                i = 0
                while i + _SILERO_FRAMES <= len(all_samples):
                    chunk = all_samples[i : i + _SILERO_FRAMES]
                    float_buf = bytearray(
                        struct.pack(
                            f"<{_SILERO_FRAMES}f",
                            *(s / 32768.0 for s in chunk),
                        )
                    )
                    prob = _vad_model_sync.process(float_buf)
                    if prob >= speech_threshold:
                        detected = True
                    i += _SILERO_FRAMES
                if i < len(all_samples):
                    _vad_leftover_samples_sync.extend(all_samples[i:])
                return detected
        else:
            _rms_thresh = int(speech_threshold * 160) if speech_threshold <= 1.0 else int(speech_threshold)
            if _rms_thresh < 1:
                _rms_thresh = 80

            def has_speech(frame: bytes) -> bool:  # type: ignore[misc]
                if not frame:
                    return False
                if _audioop is None:
                    return True
                try:
                    return _audioop.rms(frame, sample_width) >= _rms_thresh
                except Exception:
                    return False

        def buffered_duration_seconds() -> float:
            return len(buffer) / bytes_per_second

        def sanitize_frame(frame: bytes) -> bytes:
            remainder = len(frame) % sample_width
            if remainder == 0:
                return frame
            return frame[: len(frame) - remainder]

        if incremental:
            chunk_bytes_limit = int(max_chunk_seconds * bytes_per_second)
            overlap_seconds = tail_context_seconds or 2.0
            overlap_bytes = int(overlap_seconds * bytes_per_second)

            audio_buf = bytearray()
            speech_detected = False
            trailing_silence_seconds = 0.0
            chunk_index = 0
            committed_text = ""
            prev_transcript = ""

            def transcribe_chunk(
                chunk_bytes: bytes,
            ) -> Generator[Union[Dict[str, Any], str], None, str]:
                nonlocal chunk_index
                wav_chunk = _pcm_to_wav_bytes(
                    chunk_bytes, sample_rate, channels, sample_width
                )
                result_text = ""
                for event in self.speech_to_text_stream(wav_chunk, request_options):
                    if emit_raw_events:
                        if isinstance(event, dict):
                            event.setdefault("chunk_index", chunk_index)
                        yield event
                    if isinstance(event, dict):
                        event_type = str(event.get("type", ""))
                        if event_type in ("transcript.done", "transcript.final"):
                            text = event.get("text")
                            if isinstance(text, str) and text.strip():
                                result_text = text.strip()
                chunk_index += 1
                return _strip_trailing_hallucination(result_text) if result_text else result_text

            def stitch_text(prev: str, current: str) -> str:
                """Find overlapping text between prev and current, return only the new portion."""
                if not prev or not current:
                    return current
                prev_tokens = _tokenize_text(prev)
                cur_tokens = _tokenize_text(current)
                overlap = _find_token_overlap(prev_tokens, cur_tokens)
                if overlap > 0:
                    new_tokens = cur_tokens[overlap:]
                    return _join_tokens(new_tokens) if new_tokens else ""
                return current

            for frame in audio_stream:
                if not frame:
                    continue
                frame_bytes = sanitize_frame(bytes(frame))
                if not frame_bytes:
                    continue

                duration = frame_duration_seconds(frame_bytes)
                audio_buf.extend(frame_bytes)

                if has_speech(frame_bytes):
                    speech_detected = True
                    trailing_silence_seconds = 0.0
                elif speech_detected:
                    trailing_silence_seconds += duration

                buf_seconds = len(audio_buf) / bytes_per_second
                chunk_full = speech_detected and buf_seconds >= max_chunk_seconds
                silence_flush = (
                    speech_detected
                    and buf_seconds >= min_chunk_seconds
                    and trailing_silence_seconds >= silence_flush_seconds
                )

                if chunk_full or silence_flush:
                    chunk_data = bytes(audio_buf)
                    transcript = yield from transcribe_chunk(chunk_data)

                    if transcript:
                        new_text = stitch_text(prev_transcript, transcript)
                        prev_transcript = transcript

                        if new_text:
                            committed_text = (
                                f"{committed_text} {new_text}".strip()
                                if committed_text
                                else new_text
                            )

                        if silence_flush:
                            if committed_text:
                                yield {
                                    "type": "transcript.final",
                                    "text": committed_text,
                                    "delta": new_text or "",
                                    "chunk_index": chunk_index - 1,
                                    "is_final_chunk": True,
                                }
                            audio_buf.clear()
                            speech_detected = False
                            trailing_silence_seconds = 0.0
                            committed_text = ""
                            prev_transcript = ""
                        else:
                            if committed_text:
                                yield {
                                    "type": "transcript.partial",
                                    "text": committed_text,
                                    "delta": new_text or "",
                                    "chunk_index": chunk_index - 1,
                                    "is_final_chunk": False,
                                }
                            # Keep overlap audio for stitching
                            keep = min(overlap_bytes, len(audio_buf))
                            keep -= keep % sample_width
                            audio_buf = bytearray(audio_buf[-keep:]) if keep > 0 else bytearray()

            # Flush remaining audio
            if audio_buf and speech_detected:
                chunk_data = bytes(audio_buf)
                transcript = yield from transcribe_chunk(chunk_data)
                if transcript:
                    new_text = stitch_text(prev_transcript, transcript)
                    if new_text:
                        committed_text = (
                            f"{committed_text} {new_text}".strip()
                            if committed_text
                            else new_text
                        )
                    if committed_text:
                        yield {
                            "type": "transcript.final",
                            "text": committed_text,
                            "delta": new_text or "",
                            "chunk_index": chunk_index - 1,
                            "is_final_chunk": True,
                        }
            return

        buffer = bytearray()
        speech_detected = False
        trailing_silence_seconds = 0.0
        chunk_index = 0

        def buffered_duration_seconds() -> float:
            return len(buffer) / bytes_per_second

        def stream_chunk(chunk_bytes: bytes, is_final_chunk: bool = False):
            nonlocal chunk_index
            if not chunk_bytes:
                return

            wav_chunk = _pcm_to_wav_bytes(
                chunk_bytes, sample_rate, channels, sample_width
            )

            for event in self.speech_to_text_stream(wav_chunk, request_options):
                if isinstance(event, dict):
                    event.setdefault("chunk_index", chunk_index)
                    event.setdefault("is_final_chunk", is_final_chunk)
                yield event
            chunk_index += 1

        for frame in audio_stream:
            if not frame:
                continue

            frame_bytes = sanitize_frame(bytes(frame))
            if not frame_bytes:
                continue

            duration = frame_duration_seconds(frame_bytes)
            buffer.extend(frame_bytes)

            if has_speech(frame_bytes):
                speech_detected = True
                trailing_silence_seconds = 0.0
            elif speech_detected:
                trailing_silence_seconds += duration

            buffered_seconds = buffered_duration_seconds()
            should_flush = False

            if buffered_seconds >= max_chunk_seconds:
                should_flush = True
            elif (
                speech_detected
                and buffered_seconds >= min_chunk_seconds
                and trailing_silence_seconds >= silence_flush_seconds
            ):
                should_flush = True
            if should_flush:
                # Always flush on hard max; flush early on silence only after speech detection.
                if speech_detected or buffered_seconds >= max_chunk_seconds:
                    yield from stream_chunk(bytes(buffer), is_final_chunk=False)
                buffer.clear()
                speech_detected = False
                trailing_silence_seconds = 0.0

        if buffer and speech_detected:
            yield from stream_chunk(bytes(buffer), is_final_chunk=True)

    @staticmethod
    def _raise_if_stream_error(resp: Any) -> None:
        if resp.status_code == 200:
            return

        try:
            error = resp.json()
            raise_for_code_and_type(
                code=resp.status_code,
                message=error.get("message"),
                err=error.get("error"),
            )
        except json.JSONDecodeError:
            raise_for_code_and_type(
                code=resp.status_code,
                message="Failed to parse response. Invalid content type or encoding.",
            )

    @staticmethod
    def _iter_sse_events(
        resp: Any,
    ) -> Generator[Union[Dict[str, Any], str], None, None]:
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:
                continue

            line = raw_line.strip()
            if not line.startswith("data:"):
                continue

            data = line[5:].strip()
            if not data:
                continue

            if data == "[DONE]":
                yield data
                break

            try:
                yield cast(Dict[str, Any], json.loads(data))
            except json.JSONDecodeError:
                yield data


class AsyncAudio(ClientConfig):
    config: AsyncRequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = AsyncRequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    async def speech_to_text(
        self, params: SpeechToTextParams
    ) -> Union[SpeechToTextResponse, SpeechToTextWebhookResponse]: ...
    @overload
    async def speech_to_text(
        self, blob: bytes, options: Optional[SpeechToTextParams] = None
    ) -> Union[SpeechToTextResponse, SpeechToTextWebhookResponse]: ...

    async def speech_to_text(
        self,
        blob: Union[SpeechToTextParams, bytes],
        options: Optional[SpeechToTextParams] = None,
    ) -> Union[SpeechToTextResponse, SpeechToTextWebhookResponse]:
        options = options or {}
        path = "/ai/transcribe"
        if isinstance(blob, dict):
            resp = await AsyncRequest(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            verb="post",
            files=files,
        ).perform_with_content()
        return resp

    @overload
    async def speech_to_text_stream(
        self, params: SpeechToTextParams
    ) -> AsyncGenerator[Union[Dict[str, Any], str], None]: ...

    @overload
    async def speech_to_text_stream(
        self, blob: bytes, options: Optional[SpeechToTextParams] = None
    ) -> AsyncGenerator[Union[Dict[str, Any], str], None]: ...

    async def speech_to_text_stream(
        self,
        blob: Union[SpeechToTextParams, bytes],
        options: Optional[SpeechToTextParams] = None,
    ) -> AsyncGenerator[Union[Dict[str, Any], str], None]:
        """
        Async stream speech-to-text events from JigsawStack using SSE (`stream=true`).
        """
        options = options or {}
        path = "/ai/transcribe"
        url = f"{self.config['base_url']}{path}"

        headers: Dict[str, str] = {
            "Accept": "application/json",
            "x-api-key": f"{self.config['api_key']}",
        }
        custom_headers = self.config.get("headers") or {}
        headers.update(custom_headers)

        request_json = None
        request_data = None

        if isinstance(blob, dict):
            params = dict(cast(Dict[str, Any], blob))
            params["stream"] = True
            request_json = params
        else:
            params = dict(cast(Dict[str, Any], options))
            params["stream"] = True
            params["by_speaker"] = False
            if not params.get("language") or params.get("language") == "auto":
                params["language"] = "en"
            params.pop("webhook_url", None)

            request_data = aiohttp.FormData()
            request_data.add_field("file", blob, filename="upload")
            request_data.add_field(
                "body", json.dumps(params), content_type="application/json"
            )
            headers.pop("Content-Type", None)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=request_json, data=request_data, headers=headers
            ) as resp:
                await self._raise_if_stream_error_async(resp)
                async for event in self._iter_sse_events_async(resp):
                    yield event

    async def live_speech_to_text(
        self,
        audio_stream: AsyncIterable[bytes],
        options: Optional[LiveSpeechToTextOptions] = None,
    ) -> AsyncGenerator[Union[Dict[str, Any], str], None]:
        """
        Async stateless live transcription helper.
        """
        opts = dict(cast(Dict[str, Any], options or {}))

        incremental = bool(opts.pop("incremental", False))
        window_seconds = float(opts.pop("window_seconds", 3.0))
        hop_seconds = float(opts.pop("hop_seconds", 0.8))
        stability_rounds = int(opts.pop("stability_rounds", 2))
        emit_raw_events = bool(opts.pop("emit_raw_events", False))
        tail_context_seconds = float(opts.pop("tail_context_seconds", 0.25))
        max_chunk_seconds = float(opts.pop("max_chunk_seconds", 3.0))
        min_chunk_seconds = float(opts.pop("min_chunk_seconds", 0.25))
        sample_rate = int(opts.pop("sample_rate", 16000))
        channels = int(opts.pop("channels", 1))
        sample_width = int(opts.pop("sample_width", 2))
        speech_threshold = float(opts.pop("speech_threshold", 0.5))
        opts.pop("silence_rms_threshold", None)
        silence_flush_seconds = float(opts.pop("silence_flush_seconds", 0.45))

        if max_chunk_seconds <= 0:
            raise ValueError("max_chunk_seconds must be > 0")
        if min_chunk_seconds < 0:
            raise ValueError("min_chunk_seconds must be >= 0")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be > 0")
        if hop_seconds <= 0:
            raise ValueError("hop_seconds must be > 0")
        if stability_rounds <= 0:
            raise ValueError("stability_rounds must be > 0")
        if tail_context_seconds < 0:
            raise ValueError("tail_context_seconds must be >= 0")
        if sample_rate <= 0:
            raise ValueError("sample_rate must be > 0")
        if channels <= 0:
            raise ValueError("channels must be > 0")
        if sample_width not in (1, 2, 4):
            raise ValueError("sample_width must be 1, 2, or 4 bytes")

        bytes_per_second = sample_rate * channels * sample_width

        request_options = cast(SpeechToTextParams, opts)
        request_options["stream"] = True
        request_options["by_speaker"] = False
        if not request_options.get("language") or request_options.get("language") == "auto":
            request_options["language"] = "en"
        request_options.pop("webhook_url", None)

        def frame_duration_seconds(frame: bytes) -> float:
            return len(frame) / bytes_per_second

        # --- VAD setup ---
        _vad_leftover_samples_async: list = []
        if _HAS_SILERO:
            _vad_model_async = _SileroVAD(sample_rate)
            _SILERO_FRAMES_A = 512

            def has_speech(frame: bytes) -> bool:
                if not frame:
                    return False
                n_samples = len(frame) // 2
                samples = struct.unpack(f"<{n_samples}h", frame[: n_samples * 2])
                all_samples = _vad_leftover_samples_async + list(samples)
                _vad_leftover_samples_async.clear()
                detected = False
                i = 0
                while i + _SILERO_FRAMES_A <= len(all_samples):
                    chunk = all_samples[i : i + _SILERO_FRAMES_A]
                    float_buf = bytearray(
                        struct.pack(
                            f"<{_SILERO_FRAMES_A}f",
                            *(s / 32768.0 for s in chunk),
                        )
                    )
                    prob = _vad_model_async.process(float_buf)
                    if prob >= speech_threshold:
                        detected = True
                    i += _SILERO_FRAMES_A
                if i < len(all_samples):
                    _vad_leftover_samples_async.extend(all_samples[i:])
                return detected
        else:
            _rms_thresh_a = int(speech_threshold * 160) if speech_threshold <= 1.0 else int(speech_threshold)
            if _rms_thresh_a < 1:
                _rms_thresh_a = 80

            def has_speech(frame: bytes) -> bool:  # type: ignore[misc]
                if not frame:
                    return False
                if _audioop is None:
                    return True
                try:
                    return _audioop.rms(frame, sample_width) >= _rms_thresh_a
                except Exception:
                    return False

        def buffered_duration_seconds() -> float:
            return len(buffer) / bytes_per_second

        def sanitize_frame(frame: bytes) -> bytes:
            remainder = len(frame) % sample_width
            if remainder == 0:
                return frame
            return frame[: len(frame) - remainder]

        if incremental:
            chunk_bytes_limit = int(max_chunk_seconds * bytes_per_second)
            overlap_seconds = tail_context_seconds or 2.0
            overlap_bytes = int(overlap_seconds * bytes_per_second)

            audio_buf = bytearray()
            speech_detected = False
            trailing_silence_seconds = 0.0
            chunk_index = 0
            committed_text = ""
            prev_transcript = ""
            yield_queue: List[Union[Dict[str, Any], str]] = []

            async def transcribe_chunk(chunk_bytes: bytes) -> str:
                nonlocal chunk_index
                wav_chunk = _pcm_to_wav_bytes(
                    chunk_bytes, sample_rate, channels, sample_width
                )
                result_text = ""
                async for event in self.speech_to_text_stream(
                    wav_chunk, request_options
                ):
                    if emit_raw_events:
                        if isinstance(event, dict):
                            event.setdefault("chunk_index", chunk_index)
                        yield_queue.append(event)
                    if isinstance(event, dict):
                        event_type = str(event.get("type", ""))
                        if event_type in ("transcript.done", "transcript.final"):
                            text = event.get("text")
                            if isinstance(text, str) and text.strip():
                                result_text = text.strip()
                chunk_index += 1
                return result_text

            def stitch_text(prev: str, current: str) -> str:
                if not prev or not current:
                    return current
                prev_tokens = _tokenize_text(prev)
                cur_tokens = _tokenize_text(current)
                overlap = _find_token_overlap(prev_tokens, cur_tokens)
                if overlap > 0:
                    new_tokens = cur_tokens[overlap:]
                    return _join_tokens(new_tokens) if new_tokens else ""
                return current

            async for frame in audio_stream:
                if not frame:
                    continue
                frame_bytes = sanitize_frame(bytes(frame))
                if not frame_bytes:
                    continue

                duration = frame_duration_seconds(frame_bytes)
                audio_buf.extend(frame_bytes)

                if has_speech(frame_bytes):
                    speech_detected = True
                    trailing_silence_seconds = 0.0
                elif speech_detected:
                    trailing_silence_seconds += duration

                buf_seconds = len(audio_buf) / bytes_per_second
                chunk_full = speech_detected and buf_seconds >= max_chunk_seconds
                silence_flush = (
                    speech_detected
                    and buf_seconds >= min_chunk_seconds
                    and trailing_silence_seconds >= silence_flush_seconds
                )

                if chunk_full or silence_flush:
                    chunk_data = bytes(audio_buf)
                    transcript = await transcribe_chunk(chunk_data)

                    while yield_queue:
                        yield yield_queue.pop(0)

                    if transcript:
                        new_text = stitch_text(prev_transcript, transcript)
                        prev_transcript = transcript

                        if new_text:
                            committed_text = (
                                f"{committed_text} {new_text}".strip()
                                if committed_text
                                else new_text
                            )

                        if silence_flush:
                            if committed_text:
                                yield {
                                    "type": "transcript.final",
                                    "text": committed_text,
                                    "delta": new_text or "",
                                    "chunk_index": chunk_index - 1,
                                    "is_final_chunk": True,
                                }
                            audio_buf.clear()
                            speech_detected = False
                            trailing_silence_seconds = 0.0
                            committed_text = ""
                            prev_transcript = ""
                        else:
                            if committed_text:
                                yield {
                                    "type": "transcript.partial",
                                    "text": committed_text,
                                    "delta": new_text or "",
                                    "chunk_index": chunk_index - 1,
                                    "is_final_chunk": False,
                                }
                            keep = min(overlap_bytes, len(audio_buf))
                            keep -= keep % sample_width
                            audio_buf = bytearray(audio_buf[-keep:]) if keep > 0 else bytearray()

            # Flush remaining audio
            if audio_buf and speech_detected:
                chunk_data = bytes(audio_buf)
                transcript = await transcribe_chunk(chunk_data)
                while yield_queue:
                    yield yield_queue.pop(0)
                if transcript:
                    new_text = stitch_text(prev_transcript, transcript)
                    if new_text:
                        committed_text = (
                            f"{committed_text} {new_text}".strip()
                            if committed_text
                            else new_text
                        )
                    if committed_text:
                        yield {
                            "type": "transcript.final",
                            "text": committed_text,
                            "delta": new_text or "",
                            "chunk_index": chunk_index - 1,
                            "is_final_chunk": True,
                        }
            return

        buffer = bytearray()
        speech_detected = False
        trailing_silence_seconds = 0.0
        chunk_index = 0

        def buffered_duration_seconds() -> float:
            return len(buffer) / bytes_per_second

        async def stream_chunk(chunk_bytes: bytes, is_final_chunk: bool = False):
            nonlocal chunk_index
            if not chunk_bytes:
                return

            wav_chunk = _pcm_to_wav_bytes(
                chunk_bytes, sample_rate, channels, sample_width
            )

            async for event in self.speech_to_text_stream(wav_chunk, request_options):
                if isinstance(event, dict):
                    event.setdefault("chunk_index", chunk_index)
                    event.setdefault("is_final_chunk", is_final_chunk)
                yield event
            chunk_index += 1

        async for frame in audio_stream:
            if not frame:
                continue

            frame_bytes = sanitize_frame(bytes(frame))
            if not frame_bytes:
                continue

            duration = frame_duration_seconds(frame_bytes)
            buffer.extend(frame_bytes)

            if has_speech(frame_bytes):
                speech_detected = True
                trailing_silence_seconds = 0.0
            elif speech_detected:
                trailing_silence_seconds += duration

            buffered_seconds = buffered_duration_seconds()
            should_flush = False

            if buffered_seconds >= max_chunk_seconds:
                should_flush = True
            elif (
                speech_detected
                and buffered_seconds >= min_chunk_seconds
                and trailing_silence_seconds >= silence_flush_seconds
            ):
                should_flush = True

            if should_flush:
                # Always flush on hard max; flush early on silence only after speech detection.
                if speech_detected or buffered_seconds >= max_chunk_seconds:
                    async for event in stream_chunk(
                        bytes(buffer), is_final_chunk=False
                    ):
                        yield event
                buffer.clear()
                speech_detected = False
                trailing_silence_seconds = 0.0

        if buffer and speech_detected:
            async for event in stream_chunk(bytes(buffer), is_final_chunk=True):
                yield event

    @staticmethod
    async def _raise_if_stream_error_async(resp: aiohttp.ClientResponse) -> None:
        if resp.status == 200:
            return

        try:
            error = await resp.json()
            raise_for_code_and_type(
                code=resp.status,
                message=error.get("message"),
                err=error.get("error"),
            )
        except Exception:
            text = await resp.text()
            raise_for_code_and_type(
                code=resp.status,
                message=text
                or "Failed to parse response. Invalid content type or encoding.",
            )

    @staticmethod
    async def _iter_sse_events_async(
        resp: aiohttp.ClientResponse,
    ) -> AsyncGenerator[Union[Dict[str, Any], str], None]:
        buffer = ""

        async for chunk in resp.content.iter_chunked(1024):
            if not chunk:
                continue

            buffer += chunk.decode("utf-8", errors="ignore")

            while "\n" in buffer:
                raw_line, buffer = buffer.split("\n", 1)
                line = raw_line.strip()
                if not line.startswith("data:"):
                    continue

                data = line[5:].strip()
                if not data:
                    continue

                if data == "[DONE]":
                    yield data
                    return

                try:
                    yield cast(Dict[str, Any], json.loads(data))
                except json.JSONDecodeError:
                    yield data
