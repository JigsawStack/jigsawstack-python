
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict



class SpeechToTextParams(TypedDict):
    url:str
    file_store_key : NotRequired[str]
    language : NotRequired[str]
    translate : NotRequired[bool]
    by_speaker : NotRequired[bool]
    webhook_url : NotRequired[str]

class SpeechToTextResponse(TypedDict):
    success:bool
    text : str
    chunks : List[object]