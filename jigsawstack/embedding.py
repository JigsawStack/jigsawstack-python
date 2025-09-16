from typing import Any, Dict, List, Literal, Union, cast, overload

from typing_extensions import NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest
from .request import Request, RequestConfig


class EmbeddingParams(TypedDict):
    text: NotRequired[str]
    file_content: NotRequired[Any]
    type: Literal["text", "text-other", "image", "audio", "pdf"]
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    token_overflow_mode: NotRequired[Literal["truncate", "error"]]


class Chunk(TypedDict):
    text: str
    timestamp: List[int]


class EmbeddingResponse(BaseResponse):
    embeddings: List[List[float]]
    chunks: Union[List[Chunk], List[str]]


class Embedding(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    def execute(self, params: EmbeddingParams) -> EmbeddingResponse: ...
    @overload
    def execute(self, blob: bytes, options: EmbeddingParams = None) -> EmbeddingResponse: ...

    def execute(
        self,
        blob: Union[EmbeddingParams, bytes],
        options: EmbeddingParams = None,
    ) -> EmbeddingResponse:
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


class AsyncEmbedding(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    async def execute(self, params: EmbeddingParams) -> EmbeddingResponse: ...
    @overload
    async def execute(self, blob: bytes, options: EmbeddingParams = None) -> EmbeddingResponse: ...

    async def execute(
        self,
        blob: Union[EmbeddingParams, bytes],
        options: EmbeddingParams = None,
    ) -> EmbeddingResponse:
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
