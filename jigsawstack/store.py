from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from .helpers import build_path
from .exceptions import JigsawStackError
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
    temp_public_url: NotRequired[str] # Optional, only if temp_public_url is set to True in params
    

class Store(ClientConfig):

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

    def upload(self, file: bytes, options: Union[FileUploadParams, None] = None) -> FileUploadResponse:
        if options is None:
            options = {}
            
        path = build_path(base_path="/store/file", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        
        _headers = {"Content-Type": content_type}

        resp = Request(
            config=self.config,
            params=options,  # Empty params since we're using them in the URL
            path=path,
            data=file,
            headers=_headers,
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
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = AsyncRequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )
        

    async def upload(self, file: bytes, options: Union[FileUploadParams, None] = None) -> FileUploadResponse:
        if options is None:
            options = {}
            
        path = build_path(base_path="/store/file", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        _headers = {"Content-Type": content_type}
        resp = await AsyncRequest(
            config=self.config,
            params=options,  # Empty params since we're using them in the URL
            path=path,
            data=file,
            headers=_headers,
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
