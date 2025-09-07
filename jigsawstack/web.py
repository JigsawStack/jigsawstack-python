from typing import Any, Dict, List, Union, Optional, cast, Literal, overload
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
    DeepResearchParams,
    DeepResearchResponse,
)
from ._types import BaseResponse


class GotoOptions(TypedDict):
    timeout: NotRequired[int]
    wait_until: NotRequired[
        Literal["load", "domcontentloaded", "networkidle0", "networkidle2"]
    ]


#
# HTML to Any
#
class HTMLToAnyParams(TypedDict):
    html: NotRequired[str]
    url: NotRequired[str]
    goto_options: NotRequired[GotoOptions]
    full_page: NotRequired[bool]
    omit_background: NotRequired[bool]
    type: NotRequired[Literal["pdf", "png", "jpeg", "webp"]]
    width: NotRequired[int]
    height: NotRequired[int]
    scale: NotRequired[int]
    is_mobile: NotRequired[bool]
    dark_mode: NotRequired[bool]
    use_graphic_renderer: NotRequired[bool]
    size_preset: NotRequired[str]
    pdf_display_header_footer: NotRequired[bool]
    pdf_print_background: NotRequired[bool]
    pdf_page_range: NotRequired[str]
    quality: NotRequired[int]


class HTMLToAnyURLParams(HTMLToAnyParams):
    return_type: NotRequired[Literal["url", "base64"]]


class HTMLToAnyBinaryParams(HTMLToAnyParams):
    return_type: NotRequired[Literal["binary"]]


# Response types for different return_type values
class HTMLToAnyURLResponse(BaseResponse):
    """Response for 'url' and 'base64' return types"""

    url: str


# For binary responses, we return the raw bytes
HTMLToAnyBinaryResponse = bytes


class HTMLToAnyResponse(BaseResponse):
    url: str


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


class WaitFor(TypedDict):
    mode: Literal["selector", "timeout", "function"]
    value: Union[str, int]


class AdvanceConfigParams(TypedDict):
    console: NotRequired[bool]
    network: NotRequired[bool]
    cookies: NotRequired[bool]


class BYOProxyAuth(TypedDict):
    username: str
    password: str


class BYOProxy(TypedDict):
    server: str
    auth: NotRequired[BYOProxyAuth]


class BaseAIScrapeParams(TypedDict):
    url: NotRequired[str]
    html: NotRequired[str]
    http_headers: NotRequired[Dict[str, Any]]
    reject_request_pattern: NotRequired[List[str]]
    goto_options: NotRequired[GotoOptions]
    wait_for: NotRequired[WaitFor]
    advance_config: NotRequired[AdvanceConfigParams]
    size_preset: NotRequired[str]
    is_mobile: NotRequired[bool]
    scale: NotRequired[int]
    width: NotRequired[int]
    height: NotRequired[int]
    cookies: NotRequired[List[CookieParameter]]
    force_rotate_proxy: NotRequired[bool]
    byo_proxy: NotRequired[BYOProxy]
    features: NotRequired[List[Literal["meta", "link"]]]
    selectors: NotRequired[List[str]]


class AIScrapeParams(BaseAIScrapeParams):
    element_prompts: NotRequired[List[str]]
    root_element_selector: NotRequired[str]
    page_position: NotRequired[int]


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


class NetworkItem(TypedDict):
    url: str
    method: str
    status: int
    headers: Dict[str, str]
    body: Optional[str]
    type: Literal["request", "response"]


class AdvanceConfigResponse(TypedDict):
    console: NotRequired[Any]
    network: NotRequired[NetworkItem]
    cookies: NotRequired[Any]


class AIScrapeResponse(BaseResponse):
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

    @overload
    def html_to_any(self, params: HTMLToAnyURLParams) -> HTMLToAnyURLResponse: ...

    @overload
    def html_to_any(self, params: HTMLToAnyBinaryParams) -> HTMLToAnyBinaryResponse: ...

    def html_to_any(
        self, params: HTMLToAnyParams
    ) -> Union[HTMLToAnyURLResponse, HTMLToAnyBinaryResponse]:
        path = "/web/html_to_any"
        return_type = params.get("return_type", "url")

        if return_type == "binary":
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content_file()
            return cast(HTMLToAnyBinaryResponse, resp)
        else:  # "url" or "base64"
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content()
            return cast(HTMLToAnyURLResponse, resp)

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

    def deep_research(self, params: DeepResearchParams) -> DeepResearchResponse:
        s = Search(
            self.api_key,
            self.api_url,
            disable_request_logging=self.config.get("disable_request_logging"),
        )
        return s.deep_research(params)


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
        self.config = AsyncRequestConfig(
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

    @overload
    async def html_to_any(self, params: HTMLToAnyURLParams) -> HTMLToAnyURLResponse: ...

    @overload
    async def html_to_any(
        self, params: HTMLToAnyBinaryParams
    ) -> HTMLToAnyBinaryResponse: ...

    async def html_to_any(
        self, params: HTMLToAnyParams
    ) -> Union[HTMLToAnyURLResponse, HTMLToAnyBinaryResponse]:
        path = "/web/html_to_any"
        return_type = params.get("return_type", "url")

        if return_type == "binary":
            resp = await AsyncRequest(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content_file()
            return cast(HTMLToAnyBinaryResponse, resp)
        else:  # "url" or "base64"
            resp = await AsyncRequest(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content()
            return cast(HTMLToAnyURLResponse, resp)

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

    async def deep_research(self, params: DeepResearchParams) -> DeepResearchResponse:
        s = AsyncSearch(
            self.api_key,
            self.api_url,
            disable_request_logging=self.config.get("disable_request_logging"),
        )
        return await s.deep_research(params)
