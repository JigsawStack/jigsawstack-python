from typing import Any, Dict, List, Union, cast, Literal
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest
from typing import List, Union
from ._config import ClientConfig


class SummaryParams(TypedDict):
    text: Union[str, List[str]]
    """
    The text to summarize.
    """

    type: NotRequired[Literal["text", "points"]]

    """
   The summary result type. Supported values are: text, points
    """
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    max_points: NotRequired[int]
    max_characters: NotRequired[int]


class SummaryResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    summary: str
    """
    The summarized text.
    """


class SummaryListResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    summary: List[str]
    """
    The summarized text.
    """


class Summary(ClientConfig):

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

    def summarize(
        self, params: SummaryParams
    ) -> Union[SummaryResponse, SummaryListResponse]:
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
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    async def summarize(
        self, params: SummaryParams
    ) -> Union[SummaryResponse, SummaryListResponse]:
        path = "/ai/summary"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
