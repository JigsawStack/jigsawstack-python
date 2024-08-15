from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._kv import KVAddParams, KVAddResponse, KVGetResponse

class KV:
    @classmethod
    def add(cls, params: KVAddParams) -> KVAddResponse:
        path = "/store/kv"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    @classmethod
    def get(cls, key: str) -> KVGetResponse:
        path =f"/store/kv/{key}"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params={}), verb="get"
        ).perform_with_content()
        return resp
    @classmethod
    def delete(cls, key: str) -> KVGetResponse:
        path =f"/store/kv/{key}"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params={}), verb="delete"
        ).perform_with_content()
        return resp