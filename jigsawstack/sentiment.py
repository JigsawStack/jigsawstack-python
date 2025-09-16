from typing import Any, Dict, List, Union, cast

from typing_extensions import TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest
from .request import Request, RequestConfig


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


class SentimentResponse(BaseResponse):
    sentiment: SentimentResult


class Sentiment(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
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


class AsyncSentiment(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    async def analyze(self, params: SentimentParams) -> SentimentResponse:
        path = "/ai/sentiment"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
