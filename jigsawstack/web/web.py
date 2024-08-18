from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from ..request import Request
from ._web import ScrapeParams, AIScrapeParams, ScrapeResponse,HTMLToAnyParams,DNSResponse, DNSParams
from .search import AISearchParams, SearchAIResponse, SearchSuggestionParams, SearchSuggestionResponse
from .._config import ClientConfig


class Search(ClientConfig):
    def ai_search(self, params: AISearchParams) -> SearchAIResponse:
        path = "/web/search"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    

    def suggestion(self, params: SearchSuggestionParams) -> SearchSuggestionResponse:
        path = "/web/search/suggest"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp

class Web(ClientConfig):

    def ai_scrape(self, params: AIScrapeParams) -> ScrapeResponse:
        path = "/ai/scrape"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    def scrape(self, params: ScrapeParams) -> ScrapeResponse:
        path = "/web/scrape"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    
    def html_to_any(self, params: HTMLToAnyParams) -> Any:
        path = "/web/html_to_any"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    def dns(self, params: DNSParams) -> DNSResponse:
        domain = params.get('domain', "")
        type = params.get('type',"A")
        path = f"/web/html_to_any?domain={domain}&type={type}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp