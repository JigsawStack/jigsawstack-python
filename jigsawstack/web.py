from typing import Any, Dict, List, cast, Union
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from ._config import ClientConfig
from .search import (
    Search,
    SearchParams,
    SearchSuggestionParams,
    SearchSuggestionResponse,
    SearchResponse,
)


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


class AIScrapeParams(TypedDict):
    url: str
    element_prompts: List[str]
    type: NotRequired[str]
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
    page_position: NotRequired[int]
    root_element_selector: NotRequired[str]


class ScrapeParams(TypedDict):
    url: str
    elements: List[object]
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


class ScrapeResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    data: Any


class AIScrapeResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    data: List[object]
    context: object
    page_position_length: int
    page_position: int
    selectors: object


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

    def scrape(self, params: ScrapeParams) -> ScrapeResponse:
        path = "/web/scrape"
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
        domain = params.get("domain", "")
        type = params.get("type", "A")
        path = f"/web/html_to_any?domain={domain}&type={type}"
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

    def search_suggestion(
        self, params: SearchSuggestionParams
    ) -> SearchSuggestionResponse:
        s = Search(
            self.api_key,
            self.api_url,
            disable_request_logging=self.config.get("disable_request_logging"),
        )
        return s.suggestion(params)
