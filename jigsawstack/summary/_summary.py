from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from typing import List, Union

class SummaryParams(TypedDict):
    text: str
    """
    The text to summarize.
    """

    type: NotRequired[str]

    """
   The summary result type. Supported values are: text, points
    """

class SummaryResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    summary: str
    """
    The summarized text.
    """

def summarize(params: SummaryParams) -> SummaryResponse:
    path = "/ai/summary"
    resp = request.Request(path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
    return resp