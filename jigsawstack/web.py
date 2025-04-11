from typing import Any, Dict, List, cast, Union
from typing_extensions import NotRequired, TypedDict, Optional
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


class HTMLToAnyParams(TypedDict):
    html: str
    url: str
    goto_options: NotRequired[object]
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


class HTMLToAnyResponse(TypedDict):
    html: str


class BYOProxyAuth(TypedDict):
    username: str
    password: str


class BYOProxy(TypedDict):
    server: str
    auth: BYOProxyAuth

class BaseAIScrapeParams(TypedDict):
    url: str
    advance_config: NotRequired[object]
    size_preset: NotRequired[str]
    is_mobile: NotRequired[bool]
    scale: NotRequired[int]
    width: NotRequired[int]
    height: NotRequired[int]
    force_rotate_proxy: NotRequired[bool]
    reject_request_pattern: NotRequired[List[str]]
    http_headers: NotRequired[object]
    goto_options: NotRequired[object]
    wait_for: NotRequired[object]
    cookies: NotRequired[object]

class AIScrapeParamsWithPrompts(BaseAIScrapeParams):
    selector: Optional[List[str]]
    element_prompts: List[str]

class AIScrapeParamsWithSelector(BaseAIScrapeParams):
    selector: List[str]
    element_prompts: Optional[List[str]]

AIScrapeParams = Union[AIScrapeParamsWithSelector, AIScrapeParamsWithPrompts]

class LinkData(TypedDict):
    type: str  # "a" or "img"
    href: Optional[str]
    text: Optional[str]


class AIScrapeResponse(TypedDict):
    success: bool
    data: List[Dict[str, Any]]
    selectors: List[str]
    context: Dict[str, List[str]]
    link: List[LinkData]
    page_position: int
    page_position_length: int


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
            params=cast(AIScrapeParams, params),
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
