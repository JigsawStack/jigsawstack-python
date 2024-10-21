from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from typing import List, Union
from ._config import ClientConfig


class SentimentParams(TypedDict):
    text: str
    """
    The text.
    """


class SentimentSentenceResult(TypedDict):
    score: float
    emotion: str
    text: str
    sentiment: str


class SentimentResult(TypedDict):
    emotion: str
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
    sentences: List[SentimentSentenceResult]


class SentimentResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    sentiment: SentimentResult


class Sentiment(ClientConfig):

    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    def analyze(self, params: SentimentParams) -> SentimentResponse:
        path = "/ai/sentiment"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
