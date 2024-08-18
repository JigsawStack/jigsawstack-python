from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from ..request import Request
from ._file import FileDeleteResponse
from .._config import ClientConfig


class File(ClientConfig):
    

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