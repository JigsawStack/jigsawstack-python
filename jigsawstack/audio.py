from typing import Any, Dict, List, cast, Union, Optional, overload
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict, Literal
from .custom_typing import SupportedAccents
from .helpers import build_path


class TextToSpeechParams(TypedDict):
    text: str
    accent: NotRequired[SupportedAccents]
    speaker_clone_url: NotRequired[str]
    speaker_clone_file_store_key: NotRequired[str]
    return_type: NotRequired[Literal["url", "binary", "base64"]]


class TTSCloneParams(TypedDict):
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    name: str


class ListTTSVoiceClonesParams(TypedDict):
    limit: NotRequired[int]
    page: NotRequired[int]


class TextToSpeechResponse(TypedDict):
    success: bool
    text: str
    chunks: List[object]


class SpeechToTextParams(TypedDict):
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    language: NotRequired[str]
    translate: NotRequired[bool]
    by_speaker: NotRequired[bool]
    webhook_url: NotRequired[str]
    batch_size: NotRequired[int]
    chunk_duration: NotRequired[int]


class ChunkParams(TypedDict):
    text: str
    timestamp: tuple[int, int]


class BySpeakerParams(ChunkParams):
    speaker: str


class SpeechToTextResponse(TypedDict):
    success: bool
    text: str
    chunks: List[ChunkParams]
    speakers: Optional[List[BySpeakerParams]]


class Audio(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    @overload
    def speech_to_text(self, params: SpeechToTextParams) -> SpeechToTextResponse: ...
    @overload
    def speech_to_text(self, file: bytes, options: Optional[SpeechToTextParams] = None) -> SpeechToTextResponse: ...

    def speech_to_text(self, blob: Union[SpeechToTextParams, bytes], options: Optional[SpeechToTextParams] = None) -> SpeechToTextResponse:
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = Request(
                config=self.config,
                path="/ai/transcribe",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/ai/transcribe", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = Request(config=self.config, path=path, params=options, data=blob, headers=headers, verb="post").perform_with_content()
        return resp

    def text_to_speech(self, params: TextToSpeechParams) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def speaker_voice_accents(self) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = Request(config=self.config, path=path, params={}, verb="get").perform_with_content()
        return resp

    def create_clone(self, params: TTSCloneParams) -> TextToSpeechResponse:
        path = "/ai/tts/clone"
        resp = Request(config=self.config, path=path, params=cast(Dict[Any, Any], params), verb="post").perform_with_content()

        return resp

    def list_clones(self, params: ListTTSVoiceClonesParams) -> TextToSpeechResponse:
        path = "/ai/tts/clone"
        resp = Request(config=self.config, path=path, params=cast(Dict[Any, Any], params), verb="get").perform_with_content()
        return resp

    def delete_clone(self, voice_id: str) -> TextToSpeechResponse:
        path = f"/ai/tts/clone/{voice_id}"
        resp = Request(config=self.config, path=path, params={}, verb="delete").perform_with_content()
        return resp


class AsyncAudio(ClientConfig):
    config: AsyncRequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = AsyncRequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    @overload
    async def speech_to_text(self, params: SpeechToTextParams) -> SpeechToTextResponse: ...
    @overload
    async def speech_to_text(
        self, file: bytes, options: Optional[SpeechToTextParams] = None
    ) -> SpeechToTextResponse: ...

    async def speech_to_text(
        self,
        blob: Union[SpeechToTextParams, bytes],
        options: Optional[SpeechToTextParams] = None,
    ) -> SpeechToTextResponse:
        if isinstance(blob, dict):
            resp = await AsyncRequest(
                config=self.config,
                path="/ai/transcribe",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/ai/transcribe", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
            verb="post",
        ).perform_with_content()
        return resp

    async def text_to_speech(self, params: TextToSpeechParams) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    async def speaker_voice_accents(self) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp

    async def create_clone(self, params: TTSCloneParams) -> TextToSpeechResponse:
        path = "/ai/tts/clone"
        resp = await AsyncRequest(
            config=self.config, 
            path=path, 
            params=cast(Dict[Any, Any], params), 
            verb="post"
        ).perform_with_content()
        return resp

    async def list_clones(self, params: ListTTSVoiceClonesParams) -> TextToSpeechResponse:
        path = "/ai/tts/clone"
        resp = await AsyncRequest(
            config=self.config, 
            path=path, 
            params=cast(Dict[Any, Any], params), 
            verb="get"
        ).perform_with_content()
        return resp

    async def delete_clone(self, voice_id: str) -> TextToSpeechResponse:
        path = f"/ai/tts/clone/{voice_id}"
        resp = await AsyncRequest(
            config=self.config, 
            path=path, 
            params={}, 
            verb="delete"
        ).perform_with_content()
        return resp
