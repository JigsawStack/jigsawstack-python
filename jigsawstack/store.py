from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict


class FileDeleteResponse(TypedDict):
    success: bool


class KVGetParams(TypedDict):
    key: str


class KVGetResponse(TypedDict):
    success: bool
    value: str


class KVAddParams(TypedDict):
    key: str
    value: str
    encrypt: NotRequired[bool]
    byo_secret: NotRequired[str]


class KVAddResponse(TypedDict):
    success: bool


class FileUploadParams(TypedDict):
    overwrite: bool
    filename: str
    content_type: NotRequired[str]


class KV(ClientConfig):

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

    def add(self, params: KVAddParams) -> KVAddResponse:
        path = "/store/kv"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def get(self, key: str) -> KVGetResponse:
        path = f"/store/kv/{key}"
        resp = Request(config=self.config, path=path, verb="get").perform_with_content()
        return resp

    def delete(self, key: str) -> KVGetResponse:
        path = f"/store/kv/{key}"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params={}),
            verb="delete",
        ).perform_with_content()
        return resp


class Store(ClientConfig):

    config: RequestConfig
    kv: KV

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

        self.kv = KV(api_key, api_url, disable_request_logging)

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
        path = f"/store/file/{key}"
        resp = Request(
            config=self.config,
            path=path,
            params=None,
            verb="get",
        ).perform_with_content_file()
        return resp

    def delete(self, key: str) -> FileDeleteResponse:
        path = f"/store/file/{key}"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params={}),
            verb="delete",
        ).perform_with_content()
        return resp


class AsyncKV(ClientConfig):

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

    async def add(self, params: KVAddParams) -> KVAddResponse:
        path = "/store/kv"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    async def get(self, key: str) -> KVGetResponse:
        path = f"/store/kv/{key}"
        resp = await AsyncRequest(
            config=self.config, path=path, verb="get", params={}
        ).perform_with_content()
        return resp

    async def delete(self, key: str) -> KVGetResponse:
        path = f"/store/kv/{key}"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params={}),
            verb="delete",
        ).perform_with_content()
        return resp


class AsyncStore(ClientConfig):
    config: AsyncRequestConfig
    kv: AsyncKV

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
        self.kv = AsyncKV(api_key, api_url, disable_request_logging)

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
        path = f"/store/file/{key}"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=None,
            verb="get",
        ).perform_with_content_file()
        return resp

    async def delete(self, key: str) -> FileDeleteResponse:
        path = f"/store/file/{key}"
        resp = AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params={}),
            verb="delete",
        ).perform_with_content()
        return resp
