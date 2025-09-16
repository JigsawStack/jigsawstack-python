from typing import Any, Dict, List, Literal, Union, cast, overload

from typing_extensions import NotRequired, TypedDict

from ._config import ClientConfig
from .async_request import AsyncRequest
from .embedding import Chunk
from .request import Request, RequestConfig


class EmbeddingV2Params(TypedDict):
    text: NotRequired[str]
    file_content: NotRequired[Any]
    type: Literal["text", "text-other", "image", "audio", "pdf"]
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    token_overflow_mode: NotRequired[Literal["truncate", "error"]]
    speaker_fingerprint: NotRequired[bool]


class EmbeddingV2Response(TypedDict):
    success: bool
    embeddings: List[List[float]]
    chunks: Union[List[str], List[Chunk]]
    speaker_embeddings: List[List[float]]


class EmbeddingV2(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, api_url, headers)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    def execute(self, params: EmbeddingV2Params) -> EmbeddingV2Response: ...
    @overload
    def execute(self, blob: bytes, options: EmbeddingV2Params = None) -> EmbeddingV2Response: ...

    def execute(
        self,
        blob: Union[EmbeddingV2Params, bytes],
        options: EmbeddingV2Params = None,
    ) -> EmbeddingV2Response:
        path = "/embedding"
        options = options or {}
        if isinstance(blob, dict):
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
            files=files,
            verb="post",
        ).perform_with_content()
        return resp


class AsyncEmbeddingV2(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, api_url, headers)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    async def execute(self, params: EmbeddingV2Params) -> EmbeddingV2Response: ...
    @overload
    async def execute(
        self, blob: bytes, options: EmbeddingV2Params = None
    ) -> EmbeddingV2Response: ...

    async def execute(
        self,
        blob: Union[EmbeddingV2Params, bytes],
        options: EmbeddingV2Params = None,
    ) -> EmbeddingV2Response:
        path = "/embedding"
        options = options or {}
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
            files=files,
            verb="post",
        ).perform_with_content()
        return resp
