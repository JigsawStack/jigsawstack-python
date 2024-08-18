from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._kv import KVAddParams, KVAddResponse, KVGetResponse
from .._config import ClientConfig


class KV(ClientConfig):
 
    def add(self, params: KVAddParams) -> KVAddResponse:
        path = "/store/kv"
        resp = request.Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    def get(self, key: str) -> KVGetResponse:
        path =f"/store/kv/{key}"
        resp = request.Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params={}), verb="get"
        ).perform_with_content()
        return resp
    

    def delete(self, key: str) -> KVGetResponse:
        path =f"/store/kv/{key}"
        resp = request.Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params={}), verb="delete"
        ).perform_with_content()
        return resp