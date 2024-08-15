from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._vision import VOCRParams, OCRResponse,OCRParams

class Vision:
    @classmethod
    def vocr(cls, params: VOCRParams) -> OCRResponse:
        path = "/ai/vocr"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    @classmethod
    def object_detection(cls, params: OCRParams) -> OCRResponse:
        path = "/ai/object_detection"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp