from typing import Any, Dict, List, Union, cast, Optional
from typing_extensions import NotRequired, TypedDict
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig


class OCRParams(TypedDict):
    url: NotRequired[str]
    file_store_key: NotRequired[str]


class VOCRParams(TypedDict):
    prompt: Union[str, List[str]]
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    page_range: NotRequired[List[int]]


class OCRResponse(TypedDict):
    success: bool
    context: str
    width: int
    height: int
    tags: List[str]
    has_text: bool
    sections: List[object]
    total_pages: Optional[int]  # Only available for PDFs
    page_ranges: Optional[
        List[int]
    ]  # Only available if page_ranges is set in the request parameters.


class Vision(ClientConfig):

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

    def vocr(self, params: VOCRParams) -> OCRResponse:
        path = "/vocr"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def object_detection(self, params: OCRParams) -> OCRResponse:
        path = "/ai/object_detection"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp


class AsyncVision(ClientConfig):
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

    async def vocr(self, params: VOCRParams) -> OCRResponse:
        path = "/vocr"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    async def object_detection(self, params: OCRParams) -> OCRResponse:
        path = "/ai/object_detection"
        resp = AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
