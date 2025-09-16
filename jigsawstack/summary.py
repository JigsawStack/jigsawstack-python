from typing import Any, Dict, List, Literal, Union, cast

from typing_extensions import NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest
from .request import Request, RequestConfig


class SummaryParams(TypedDict):
    text: NotRequired[str]
    """
    The text to summarize.
    """

    type: NotRequired[Literal["text", "points"]]

    """
   The summary result type. Supported values are: text, points
    """
    url: NotRequired[str]
    """
    The URL to summarize.
    """

    file_store_key: NotRequired[str]
    """
    The file store key to summarize.
    """

    max_points: NotRequired[int]
    """
    The maximum number of points of summary.
    """

    max_characters: NotRequired[int]
    """
    The maximum number of characters of summary.
    """


class SummaryResponse(BaseResponse):
    summary: Union[str, List[str]]
    """
    The summarized text.
    """


class Summary(ClientConfig):
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

    def summarize(self, params: SummaryParams) -> SummaryResponse:
        path = "/ai/summary"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp


class AsyncSummary(ClientConfig):
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

    async def summarize(self, params: SummaryParams) -> SummaryResponse:
        path = "/ai/summary"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
