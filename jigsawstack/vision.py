from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from ._config import ClientConfig


class OCRParams(TypedDict):
    url: NotRequired[str]
    file_store_key: NotRequired[str]


class VOCRParams(TypedDict):
    prompt: str
    url: NotRequired[str]
    file_store_key: NotRequired[str]


class OCRResponse(TypedDict):
    success: bool
    context: str
    width: int
    height: int
    tags: List[str]
    has_text: bool
    sections: List[object]


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
