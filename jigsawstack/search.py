from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from typing_extensions import NotRequired, TypedDict
from ._config import ClientConfig


class SearchResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    results: List[Any]

    is_safe: bool

    ai_overview: str

    spell_fixed: str


class SearchSuggestionsResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """

    suggestions: List[str]


class SearchSuggestionsParams(TypedDict):
    query: str
    """
    The search value. The maximum query character length is 200.
    """


class SearchParams(TypedDict):
    query: str
    """
    The search value. The maximum query character length is 200.
    """
    ai_overview: NotRequired[bool] = True
    """
    Include AI powered overview in the search results. The default value is True
    """
    safe_search: NotRequired[str] = "moderate"
    """
    Include offensive results in the search results. The default value is "moderate". Supported values:  moderate, strict, off
    """
    spell_check: NotRequired[bool] = True
    """
    Spell check the search query.
    """

    byo_urls: NotRequired[List[str]]


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
