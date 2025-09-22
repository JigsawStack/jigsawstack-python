from typing import Any, Dict, List, Optional, Union, cast, overload

from typing_extensions import Literal, NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest, AsyncRequestConfig
from .request import Request, RequestConfig


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

    language_detected: Optional[str]
    """
    the language detected in the transcription, available if language is set to auto
    """

    confidence: Optional[float]
    """
    the confidence of the transcription language detection, available if language is set to auto
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
