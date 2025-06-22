from typing import Any, Dict, List, Union, cast, Literal
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from typing_extensions import NotRequired, TypedDict
from ._config import ClientConfig


class SearchResponse(TypedDict):
    success: bool
    """
    Whether the search request was successful
    """

    query: str
    """
    The search query that was used
    """

    ai_overview: str
    """
    AI-generated overview/summary of the search results
    or deep research results if enabled
    """

    results: List[Any]
    """
    List of search result items
    """

    is_safe: bool
    """
    Whether the search results passed safe search filtering
    """

    spell_fixed: bool
    """
    Whether the query was spell-checked and fixed
    """

    geo_results: List[Any]
    """
    List of location/geographic search results if applicable
    """

    image_urls: List[str]
    """
    List of image URLs found in the search results
    """

    links: List[str]
    """
    List of web page URLs found in the search results
    """


class SearchSuggestionsResponse(TypedDict):
    success: bool
    """
    Whether the search suggestions request was successful
    """

    suggestions: List[str]
    """
    List of search suggestions
    """


class SearchSuggestionsParams(TypedDict):
    query: str
    """
    The search value. The maximum query character length is 200.
    """

class DeepResearchConfig(TypedDict):
    max_depth: NotRequired[int]
    max_breadth: NotRequired[int]
    max_output_tokens: NotRequired[int]
    target_output_tokens: NotRequired[int]

class SearchParams(TypedDict):
    query: str
    """
    The search query string to execute
    """

    spell_check: NotRequired[bool]
    """
    Whether to perform spell checking on the query. Defaults to True.
    """

    safe_search: NotRequired[Literal["strict", "moderate", "off"]]
    """
    Safe search filtering level. Can be 'strict', 'moderate', or 'off'
    """

    ai_overview: NotRequired[bool]
    """
    Whether to generate an AI-powered overview of the search results. Defaults to True.
    """

    byo_urls: NotRequired[List[str]]
    """
    List of custom URLs to include in the search results
    """

    country_code: NotRequired[str]
    """
    Two-letter country code to localize search results (e.g. 'US', 'GB')
    """

    auto_scrape: NotRequired[bool]
    """
    Whether to automatically scrape content from search result URLs
    """

    deep_research: NotRequired[bool]
    """
    Enable deep research mode for more comprehensive results
    """

    deep_research_config: NotRequired[DeepResearchConfig]
    """
    Configuration options for deep research mode
    """




class Search(ClientConfig):
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

    def search(self, params: SearchParams) -> SearchResponse:
        query = params["query"]
        ai_overview = params.get("ai_overview", "True")
        safe_search = params.get("safe_search", "moderate")
        spell_check = params.get("spell_check", "True")

        body = {
            "byo_urls": params.get("byo_urls", []),
            "query": query,
            "ai_overview": ai_overview,
            "safe_search": safe_search,
            "spell_check": spell_check,
        }

        path = f"/web/search"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], body),
            verb="POST",
        ).perform_with_content()

        return resp

    def suggestions(self, params: SearchSuggestionsParams) -> SearchSuggestionsResponse:
        query = params["query"]
        path = f"/web/search/suggest?query={query}"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="GET",
        ).perform_with_content()
        return resp


class AsyncSearch(ClientConfig):
    config: AsyncRequestConfig

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

    async def search(self, params: SearchParams) -> SearchResponse:
        path = f"/web/search"
        query = params["query"]
        ai_overview = params.get("ai_overview", "True")
        safe_search = params.get("safe_search", "moderate")
        spell_check = params.get("spell_check", "True")

        body = {
            "byo_urls": params.get("byo_urls", []),
            "query": query,
            "ai_overview": ai_overview,
            "safe_search": safe_search,
            "spell_check": spell_check,
        }
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], body),
            verb="POST",
        ).perform_with_content()
        return resp

    async def suggestions(
        self, params: SearchSuggestionsParams
    ) -> SearchSuggestionsResponse:
        query = params["query"]
        path = f"/web/search/suggest?query={query}"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="GET",
        ).perform_with_content()
        return resp
