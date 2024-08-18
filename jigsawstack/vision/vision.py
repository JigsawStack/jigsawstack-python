from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from ..request import Request
from ._vision import VOCRParams, OCRResponse,OCRParams
from .._config import ClientConfig
class Vision(ClientConfig):
    def vocr(self, params: VOCRParams) -> OCRResponse:
        path = "/ai/vocr"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    def object_detection(self, params: OCRParams) -> OCRResponse:
        path = "/ai/object_detection"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp