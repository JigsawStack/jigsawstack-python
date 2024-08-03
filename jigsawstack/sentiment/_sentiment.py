from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from typing import List, Union



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

def sentiment(params: SentimentParams) -> SentimentResponse:
    path = "/ai/sentiment"
    resp = request.Request(path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
    return resp