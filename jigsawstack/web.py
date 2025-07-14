from typing import Any, Dict, List, Union, Optional, cast, Literal
from typing_extensions import NotRequired, TypedDict

from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from .search import (
    Search,
    SearchParams,
    SearchSuggestionsParams,
    SearchSuggestionsResponse,
    SearchResponse,
    AsyncSearch,
)
from .helpers import build_path


#
# DNS
#
class DNSParams(TypedDict):
    domain: str
    type: NotRequired[str]


class DNSResponse(TypedDict):
    success: bool
    domain: str
    type: str
    type_value: int
    records: List[object]
    DNSSEC_validation_disabled: bool
    DNSSEC_verified: bool
    recursion_available: bool
    recursion_desired: bool
    truncated: bool
    additional: List
    authority: List


#
# HTML to Any
#
class HTMLToAnyParams(TypedDict):
    html: NotRequired[str]
    url: NotRequired[str]
    goto_options: NotRequired[Dict[str, Union[int, str]]]
    scale: NotRequired[int]
    full_page: NotRequired[bool]
    omit_background: NotRequired[bool]
    quality: NotRequired[int]
    type: NotRequired[str]
    width: NotRequired[int]
    height: NotRequired[int]
    size_preset: NotRequired[str]
    pdf_display_header_footer: NotRequired[bool]
    pdf_print_background: NotRequired[bool]
    pdf_page_range: NotRequired[str]
    is_mobile: NotRequired[bool]
    dark_mode: NotRequired[bool]
    use_graphic_renderer: NotRequired[bool]
    return_type: NotRequired[Literal["url", "binary", "base64"]]


class HTMLToAnyResponse(TypedDict):
    html: str


#
# BYO Proxy
#
class CookieParameter(TypedDict):
    name: str
    value: str
    url: NotRequired[str]
    domain: NotRequired[str]
    path: NotRequired[str]
    secure: NotRequired[bool]
    httpOnly: NotRequired[bool]
    sameSite: NotRequired[Literal["Strict", "Lax", "None"]]
    expires: NotRequired[bool]
    priority: NotRequired[str]
    sameParty: NotRequired[bool]


class GotoOptions(TypedDict):
    timeout: int
    wait_until: str


class WaitFor(TypedDict):
    mode: str
    value: Union[str, int]


class AdvanceConfigRequest(TypedDict):
    console: bool
    network: bool
    cookies: bool


class AdvanceConfigResponse(TypedDict):
    console: list
    network: list
    cookies: list


class BYOProxyAuth(TypedDict):
    username: str
    password: str


class BYOProxy(TypedDict):
    server: str
    auth: NotRequired[BYOProxyAuth]


class BaseAIScrapeParams(TypedDict):
    url: str
    root_element_selector: NotRequired[str]
    page_position: NotRequired[int]
    http_headers: NotRequired[Dict[str, Any]]
    reject_request_pattern: NotRequired[List[str]]
    goto_options: NotRequired[GotoOptions]
    wait_for: NotRequired[WaitFor]
    advance_config: NotRequired[AdvanceConfigRequest]
    size_preset: NotRequired[str]
    is_mobile: NotRequired[bool]
    scale: NotRequired[int]
    width: NotRequired[int]
    height: NotRequired[int]
    cookies: NotRequired[List[CookieParameter]]
    force_rotate_proxy: NotRequired[bool]
    byo_proxy: NotRequired[BYOProxy]


class AIScrapeParamsWithSelector(BaseAIScrapeParams):
    selectors: List[str]
    element_prompts: NotRequired[List[str]]


class AIScrapeParamsWithPrompts(BaseAIScrapeParams):
    selectors: NotRequired[List[str]]
    element_prompts: List[str]


AIScrapeParams = Union[AIScrapeParamsWithSelector, AIScrapeParamsWithPrompts]


class Attribute(TypedDict):
    name: str
    value: str


class Result(TypedDict):
    html: str
    text: str
    attributes: List[Attribute]


class DataItem(TypedDict):
    key: str
    selectors: str
    results: List[Result]


class Link(TypedDict):
    href: str
    text: Optional[str]
    type: Literal["a", "img"]


class Meta(TypedDict):
    title: Optional[str]
    description: Optional[str]
    keywords: Optional[str]
    og_image: Optional[str]


class AIScrapeResponse(TypedDict):
    success: bool
    data: List[DataItem]
    page_position: int
    page_position_length: int
    advance_config: Optional[AdvanceConfigResponse]
    context: Any
    selectors: Dict[str, List[str]]
    meta: Optional[Meta]
    link: List[Link]


#
# Web Client
#
class Web(ClientConfig):

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

    def ai_scrape(self, params: AIScrapeParams) -> AIScrapeResponse:
        path = "/ai/scrape"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def html_to_any(self, params: HTMLToAnyParams) -> Any:
        path = "/web/html_to_any"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content_file()
        return resp

    def dns(self, params: DNSParams) -> DNSResponse:
        path = build_path(
            base_path="/web/html_to_any",
            params=params,
        )
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def search(self, params: SearchParams) -> SearchResponse:
        s = Search(
            self.api_key,
            self.api_url,
            disable_request_logging=self.config.get("disable_request_logging"),
        )
        return s.search(params)

    def search_suggestions(
        self, params: SearchSuggestionsParams
    ) -> SearchSuggestionsResponse:
        s = Search(
            self.api_key,
            self.api_url,
            disable_request_logging=self.config.get("disable_request_logging"),
        )
        return s.suggestions(params)


#
# Async Web Client
#
class AsyncWeb(ClientConfig):

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

    async def ai_scrape(self, params: AIScrapeParams) -> AIScrapeResponse:
        path = "/ai/scrape"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    async def html_to_any(self, params: HTMLToAnyParams) -> Any:
        path = "/web/html_to_any"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content_file()
        return resp

    async def dns(self, params: DNSParams) -> DNSResponse:
        path = build_path(
            base_path="/web/html_to_any",
            params=params,
        )
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    async def search(self, params: SearchParams) -> SearchResponse:
        s = AsyncSearch(
            self.api_key,
            self.api_url,
            disable_request_logging=self.config.get("disable_request_logging"),
        )
        return await s.search(params)

    async def search_suggestions(
        self, params: SearchSuggestionsParams
    ) -> SearchSuggestionsResponse:
        s = AsyncSearch(
            self.api_key,
            self.api_url,
            disable_request_logging=self.config.get("disable_request_logging"),
        )
        return await s.suggestions(params)
