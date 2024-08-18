
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict


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