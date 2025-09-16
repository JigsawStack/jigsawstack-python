from typing import Any, Dict, List, Literal, Optional, Union, cast

from typing_extensions import NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest, AsyncRequestConfig
from .request import Request, RequestConfig


class RelatedIndex(TypedDict):
    text: str
    url: str


class Content(TypedDict):
    text: str
    image_urls: List[str]
    links: List[str]


class Result(TypedDict):
    title: str
    url: str
    description: str
    content: Union[str, Content]
    is_safe: bool
    site_name: str
    site_long_name: str
    age: str
    language: str
    favicon: str
    snippets: List[str]
    related_index: List[RelatedIndex]


class GeoResult(TypedDict):
    type: str
    full_address: str
    name: str
    name_preferred: str
    place_formatted: str
    postcode: NotRequired[str]
    district: NotRequired[str]
    place: NotRequired[str]
    region: NotRequired[Any]
    country: NotRequired[Any]
    language: str
    geoloc: Dict[str, Any]
    poi_category: NotRequired[str]
    additional_properties: NotRequired[Any]


class SearchResponse(BaseResponse):
    query: str
    """
    The search query that was used
    """

    ai_overview: Optional[str]
    """
    AI-generated overview/summary of the search results
    or deep research results if enabled
    """

    results: List[Result]
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

    geo_results: List[GeoResult]
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


class SearchSuggestionsResponse(BaseResponse):
    suggestions: List[str]
    """
    List of search suggestions
    """


class SearchSuggestionsParams(TypedDict):
    query: str
    """
    The search value. The maximum query character length is 200.
    """


class DeepResearchParams(TypedDict):
    query: str
    """
    The search value. The maximum query character length is 200.
    """

    spell_check: NotRequired[bool]
    """
    Whether to perform spell checking on the query.
    """

    safe_search: NotRequired[Literal["strict", "moderate", "off"]]
    """
    Safe search filtering level. Can be 'strict', 'moderate', or 'off'
    """

    country_code: NotRequired[str]
    """
    Two-letter country code to localize search results (e.g. 'US', 'GB')
    """

    max_depth: NotRequired[int]
    """
    Maximum depth for deep research
    """

    max_breadth: NotRequired[int]
    """
    Maximum breadth for deep research
    """

    max_output_tokens: NotRequired[int]
    """
    Maximum number of output tokens
    """

    target_output_tokens: NotRequired[int]
    """
    Target number of output tokens
    """


class DeepResearchResponse(BaseResponse):
    query: str
    """
    The search query that was used
    """

    results: str
    """
    The deep research results as a string
    """

    sources: List[Result]
    """
    List of source search results used for deep research
    """

    geo_results: List[GeoResult]
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


class Search(ClientConfig):
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

        path = "/web/search"
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

    def deep_research(self, params: DeepResearchParams) -> DeepResearchResponse:
        path = "/web/deep_research"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="POST",
        ).perform_with_content()
        return resp


class AsyncSearch(ClientConfig):
    config: AsyncRequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = AsyncRequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    async def search(self, params: SearchParams) -> SearchResponse:
        path = "/web/search"
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

    async def suggestions(self, params: SearchSuggestionsParams) -> SearchSuggestionsResponse:
        query = params["query"]
        path = f"/web/search/suggest?query={query}"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="GET",
        ).perform_with_content()
        return resp

    async def deep_research(self, params: DeepResearchParams) -> DeepResearchResponse:
        path = "/web/deep_research"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="POST",
        ).perform_with_content()
        return resp
