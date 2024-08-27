from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict

class FileDeleteResponse(TypedDict):
    success:bool


class KVGetParams(TypedDict):
    key:str

class KVGetResponse(TypedDict):
    success:bool
    value : str

class KVAddParams(TypedDict):
    key:str
    value :str
    encrypt : NotRequired[bool]

class KVAddResponse(TypedDict):
    success:bool



class FileUploadParams(TypedDict):
    overwrite:bool
    filename:str
    headers: Dict[str, str]



class Store(ClientConfig):
    def upload(self, file: bytes, options=FileUploadParams) -> Any:
        overwrite = options.get("overwrite")
        filename = options.get("filename")
        params = {
            "key":filename,
            "overwrite":overwrite
        }
        path =f"/store/file?overwrite={overwrite}&key={filename}"
        headers = options.get("headers")
        _headers = {"Content-Type":"application/octet-stream"}
        if headers:
            _headers.update(headers)

        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            params=params,
            path=path,  data=file, headers=_headers, verb="post"
        
        ).perform_with_content()
        return resp

    def get(self, key: str) -> Any:
        path =f"/store/file/{key}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=None, verb="get"
        ).perform_with_content_file()
        return resp

    def delete(self, key: str) -> FileDeleteResponse:
        path =f"/store/file/{key}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params={}), verb="delete"
        ).perform_with_content()
        return resp
    

class KV(ClientConfig):
 
    def add(self, params: KVAddParams) -> KVAddResponse:
        path = "/store/kv"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    def get(self, key: str) -> KVGetResponse:
        path =f"/store/kv/{key}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, verb="get"
        ).perform_with_content()
        return resp
    

    def delete(self, key: str) -> KVGetResponse:
        path =f"/store/kv/{key}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params={}), verb="delete"
        ).perform_with_content()
        return resp