
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
from ._config import ClientConfig

class OCRParams(TypedDict):
    url : NotRequired[str]
    file_store_key : NotRequired[str]

class VOCRParams(TypedDict):
    prompt:str
    url : NotRequired[str]
    file_store_key : NotRequired[str]

class OCRResponse(TypedDict):
    success:bool
    context : str
    width : int
    height : int
    tags : List[str]
    has_text : bool
    sections : List[object]

class Vision(ClientConfig):
    def vocr(self, params: VOCRParams) -> OCRResponse:
        path = "/vocr"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    def object_detection(self, params: OCRParams) -> OCRResponse:
        path = "/ai/object_detection"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp