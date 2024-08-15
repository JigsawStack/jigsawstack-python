
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict


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
