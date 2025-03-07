from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig




class FileDeleteResponse(TypedDict):
    success: bool



class FileUploadParams(TypedDict):
    overwrite: bool
    filename: str
    content_type: NotRequired[str]

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

    def upload(self, file: bytes, options=FileUploadParams) -> Any:
        overwrite = options.get("overwrite")
        filename = options.get("filename")
        params = {"key": filename, "overwrite": overwrite}
        path = f"/store/file?overwrite={overwrite}&key={filename}"
        content_type = options.get("content_type")
        _headers = {"Content-Type": "application/octet-stream"}
        if content_type is not None:
            _headers = {"Content-Type": content_type}

        resp = Request(
            config=self.config,
            params=params,
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
        

    async def upload(self, file: bytes, options=FileUploadParams) -> Any:
        overwrite = options.get("overwrite")
        filename = options.get("filename")
        params = {"key": filename, "overwrite": overwrite}
        path = f"/store/file?overwrite={overwrite}&key={filename}"
        content_type = options.get("content_type")
        _headers = {"Content-Type": "application/octet-stream"}
        if content_type is not None:
            _headers = {"Content-Type": content_type}

        resp = await AsyncRequest(
            config=self.config,
            params=params,
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
        resp = AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params={}),
            verb="delete",
        ).perform_with_content()
        return resp
