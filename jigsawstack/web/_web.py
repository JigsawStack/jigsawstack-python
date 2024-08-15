
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict



class DNSParams(TypedDict):
    domain:str
    type : NotRequired[str]



class DNSResponse(TypedDict):
    success:bool
    domain : str
    type : str
    type_value : int
    records : List[object]
    DNSSEC_validation_disabled : bool
    DNSSEC_verified : bool
    recursion_available : bool
    recursion_desired : bool
    truncated : bool
    additional : List
    authority : List



class HTMLToAnyParams(TypedDict):
    html:str
    url : str
    goto_options : NotRequired[object]
    scale : NotRequired[int]
    full_page : NotRequired[bool]
    omit_background : NotRequired[bool]
    quality : NotRequired[int]
    type: NotRequired[str]
    width : NotRequired[int]
    height : NotRequired[int]
    size_preset: NotRequired[str]
    pdf_display_header_footer : NotRequired[bool]
    pdf_print_background : NotRequired[bool]
    pdf_page_range : NotRequired[str]
    is_mobile : NotRequired[bool]
    dark_mode : NotRequired[bool]
    use_graphic_renderer : NotRequired[bool]


class HTMLToAnyResponse(TypedDict):
    html:str

class AIScrapeParams(TypedDict):
    url: str
    element_prompts : List[str]
    type: NotRequired[str]
    size_preset: NotRequired[str]
    is_mobile : NotRequired[bool]
    scale : NotRequired[int]
    width : NotRequired[int]
    height : NotRequired[int]
    force_rotate_proxy : NotRequired[bool]
    reject_request_pattern : NotRequired[List[str]]
    http_headers : NotRequired[object]
    goto_options : NotRequired[object]
    wait_for : NotRequired[object]
    cookies : NotRequired[object]



class ScrapeParams(TypedDict):
    url: str
    elements : List[object]
    advance_config : NotRequired[object]
    size_preset: NotRequired[str]
    is_mobile : NotRequired[bool]
    scale : NotRequired[int]
    width : NotRequired[int]
    height : NotRequired[int]
    force_rotate_proxy : NotRequired[bool]
    reject_request_pattern : NotRequired[List[str]]
    http_headers : NotRequired[object]
    goto_options : NotRequired[object]
    wait_for : NotRequired[object]
    cookies : NotRequired[object]

class ScrapeResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    data: Any
