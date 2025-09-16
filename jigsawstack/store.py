from typing import Any, Dict, Union

from typing_extensions import NotRequired, TypedDict

from ._config import ClientConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from .helpers import build_path
from .request import Request, RequestConfig


class FileDeleteResponse(TypedDict):
    success: bool


class FileUploadParams(TypedDict):
    overwrite: NotRequired[bool]
    key: NotRequired[str]
    content_type: NotRequired[str]
    temp_public_url: NotRequired[bool]


class FileUploadResponse(TypedDict):
    key: str
    url: str
    size: int
    temp_public_url: NotRequired[str]  # Optional, only if temp_public_url is set to True in params


class Store(ClientConfig):
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

    def upload(
        self, file: bytes, options: Union[FileUploadParams, None] = None
    ) -> FileUploadResponse:
        if options is None:
            options = {}

        path = build_path(base_path="/store/file", params=options)
        content_type = options.get("content_type", "application/octet-stream")

        config_with_headers = self.config.copy()
        if config_with_headers.get("headers") is None:
            config_with_headers["headers"] = {}
        config_with_headers["headers"]["Content-Type"] = content_type

        resp = Request(
            config=config_with_headers,
            params={},
            path=path,
            data=file,
            verb="post",
        ).perform_with_content()
        return resp

    def get(self, key: str) -> Any:
        path = f"/store/file/read/{key}"
        resp = Request(
            config=self.config,
            path=path,
            params=None,
            verb="get",
        ).perform_with_content_file()
        return resp

    def delete(self, key: str) -> FileDeleteResponse:
        path = f"/store/file/read/{key}"
        resp = Request(
            config=self.config,
            path=path,
            params=key,
            verb="delete",
        ).perform_with_content()
        return resp


class AsyncStore(ClientConfig):
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

    async def upload(
        self, file: bytes, options: Union[FileUploadParams, None] = None
    ) -> FileUploadResponse:
        if options is None:
            options = {}

        path = build_path(base_path="/store/file", params=options)
        content_type = options.get("content_type", "application/octet-stream")

        config_with_headers = self.config.copy()
        if config_with_headers.get("headers") is None:
            config_with_headers["headers"] = {}
        config_with_headers["headers"]["Content-Type"] = content_type

        resp = await AsyncRequest(
            config=config_with_headers,
            params={},
            path=path,
            data=file,
            verb="post",
        ).perform_with_content()
        return resp

    async def get(self, key: str) -> Any:
        path = f"/store/file/read/{key}"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=None,
            verb="get",
        ).perform_with_content_file()
        return resp

    async def delete(self, key: str) -> FileDeleteResponse:
        path = f"/store/file/read/{key}"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=key,
            verb="delete",
        ).perform_with_content()
        return resp
