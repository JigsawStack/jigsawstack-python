from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._web import ScrapeParams, AIScrapeParams, ScrapeResponse,HTMLToAnyParams,DNSResponse, DNSParams


class Web:
    @classmethod
    def ai_scrape(cls, params: AIScrapeParams) -> ScrapeResponse:
        path = "/ai/scrape"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    @classmethod
    def scrape(cls, params: ScrapeParams) -> ScrapeResponse:
        path = "/web/scrape"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    @classmethod
    def html_to_any(cls, params: HTMLToAnyParams) -> Any:
        path = "/web/html_to_any"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    def dns(cls, params: DNSParams) -> DNSResponse:
        path = "/web/html_to_any"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp