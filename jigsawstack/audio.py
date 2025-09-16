from typing import Any, Dict, List, Optional, Union, cast, overload

from typing_extensions import Literal, NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest, AsyncRequestConfig
from .request import Request, RequestConfig


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
