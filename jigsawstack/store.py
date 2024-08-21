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



class File(ClientConfig):
    def upload(self, file: bytes) -> Any:
        path ="/store/file"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params={}), verb="post"
        ).perform_with_content()
        return resp

    def get(self, key: str) -> Any:
        path =f"/store/file/{key}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params={}), verb="get"
        ).perform_with_content()
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
            path=path, params=cast(Dict[Any, Any], params={}), verb="get"
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