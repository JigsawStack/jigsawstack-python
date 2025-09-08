from typing import Any, Dict, List, Union, cast, Literal, overload
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest
from typing import List, Union
from ._config import ClientConfig
from .helpers import build_path
from ._types import BaseResponse


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
    def execute(self, params: EmbeddingParams) -> EmbeddingResponse: ...
    @overload
    def execute(
        self, blob: bytes, options: EmbeddingParams = None
    ) -> EmbeddingResponse: ...

    def execute(
        self,
        blob: Union[EmbeddingParams, bytes],
        options: EmbeddingParams = None,
    ) -> EmbeddingResponse:
        path = "/embedding"
        if isinstance(blob, dict):
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path=path, params=options)
        content_type = options.get("content_type", "application/octet-stream")
        _headers = {"Content-Type": content_type}

        resp = Request(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=_headers,
            verb="post",
        ).perform_with_content()
        return resp


class AsyncEmbedding(ClientConfig):
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
    async def execute(self, params: EmbeddingParams) -> EmbeddingResponse: ...
    @overload
    async def execute(
        self, blob: bytes, options: EmbeddingParams = None
    ) -> EmbeddingResponse: ...

    async def execute(
        self,
        blob: Union[EmbeddingParams, bytes],
        options: EmbeddingParams = None,
    ) -> EmbeddingResponse:
        path = "/embedding"
        if isinstance(blob, dict):
            resp = await AsyncRequest(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path=path, params=options)
        content_type = options.get("content_type", "application/octet-stream")
        _headers = {"Content-Type": content_type}

        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=_headers,
            verb="post",
        ).perform_with_content()
        return resp
