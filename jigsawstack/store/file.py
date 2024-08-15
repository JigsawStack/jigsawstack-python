from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._file import FileDeleteResponse

class File:
    
    @classmethod
    def get(cls, key: str) -> Any:
        path =f"/store/file/{key}"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params={}), verb="get"
        ).perform_with_content()
        return resp
    @classmethod
    def delete(cls, key: str) -> FileDeleteResponse:
        path =f"/store/file/{key}"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params={}), verb="delete"
        ).perform_with_content()
        return resp