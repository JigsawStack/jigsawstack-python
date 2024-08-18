from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
from typing import List, Union
from ._config import ClientConfig


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


class Summary(ClientConfig):

    def summarize(self,params: SummaryParams) -> SummaryResponse:
        path = "/ai/summary"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
        return resp