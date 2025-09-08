from typing import Any, Dict, List, cast, Union, Optional, overload
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict, Literal
from .custom_typing import SupportedAccents
from .helpers import build_path
from ._types import BaseResponse


class SpeechToTextParams(TypedDict):
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    language: NotRequired[Union[str, Literal["auto"]]]
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
    timestamp: tuple[int, int]
    text: str


class SpeechToTextResponse(BaseResponse):
    text: str
    chunks: List[ChunkParams]
    speakers: Optional[List[BySpeakerParams]]


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

        resp = Request(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
            verb="post",
        ).perform_with_content()
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
