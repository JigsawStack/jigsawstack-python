from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
from typing import List, Union
from ._config import ClientConfig


class SentimentParams(TypedDict):
    text: str
    """
    The text.
    """


class SentimentResult(TypedDict):
     emotion : str
     """
     The emotion detected in the text.
     """
     sentiment: str
     """
     The sentiment detected in the text.
     """
     score: float
     """
      The score of the sentiment.
     """

class SentimentResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    sentiment: SentimentResult


class Sentiment(ClientConfig):
    def analyze(self, params: SentimentParams) -> SentimentResponse:
        path = "/ai/sentiment"
        resp = Request(api_key=self.api_key,
            api_url=self.api_url,path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
        return resp