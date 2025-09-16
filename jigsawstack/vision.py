from typing import Any, Dict, List, Optional, Union, cast, overload

from typing_extensions import Literal, NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest, AsyncRequestConfig
from .request import Request, RequestConfig


class Point(TypedDict):
    x: int
    """
    X coordinate of the point
    """

    y: int
    """
    Y coordinate of the point
    """


class BoundingBox(TypedDict):
    top_left: Point
    """
    Top-left corner of the bounding box
    """

    top_right: Point
    """
    Top-right corner of the bounding box
    """

    bottom_left: Point
    """
    Bottom-left corner of the bounding box
    """

    bottom_right: Point
    """
    Bottom-right corner of the bounding box
    """

    width: int
    """
    Width of the bounding box
    """

    height: int
    """
    Height of the bounding box
    """


class GuiElement(TypedDict):
    bounds: BoundingBox
    """
    Bounding box coordinates of the GUI element
    """

    content: Union[str, None]
    """
    Content of the GUI element, can be null if no object detected
    """

    interactivity: bool
    """
    Interactivity of the GUI element
    """

    type: str
    """
    Type of the GUI element
    """


class DetectedObject(TypedDict):
    bounds: BoundingBox
    """
    Bounding box coordinates of the detected object
    """

    mask: NotRequired[str]
    """
    URL or base64 string depending on return_type - only present for some objects
    """


class ObjectDetectionParams(TypedDict):
    url: NotRequired[str]
    """
    URL of the image to process
    """

    file_store_key: NotRequired[str]
    """
    File store key of the image to process
    """

    prompts: NotRequired[List[str]]
    """
    List of prompts for object detection
    """

    features: NotRequired[List[Literal["object_detection", "gui"]]]
    """
    List of features to enable: object_detection, gui
    """

    annotated_image: NotRequired[bool]
    """
    Whether to return an annotated image
    """

    return_type: NotRequired[Literal["url", "base64"]]
    """
    Format for returned images: url or base64
    """

    return_masks: NotRequired[bool]
    """
    Whether to return masks for the detected objects
    """


class ObjectDetectionResponse(BaseResponse):
    annotated_image: NotRequired[str]
    """
    URL or base64 string of annotated image (included only if annotated_image=true and objects/gui_elements exist)
    """

    gui_elements: NotRequired[List[GuiElement]]
    """
    List of detected GUI elements (included only if features includes "gui")
    """

    objects: NotRequired[List[DetectedObject]]
    """
    List of detected objects (included only if features includes "object_detection")
    """

    tags: NotRequired[List[str]]
    """
    List of tags returned by the object detection model
    """


class VOCRParams(TypedDict):
    prompt: NotRequired[Union[str, List[str], Dict[str, str]]]
    url: NotRequired[str]
    file_store_key: NotRequired[str]
    page_range: NotRequired[List[int]]


class OCRResponse(BaseResponse):
    context: str
    width: int
    height: int
    tags: List[str]
    has_text: bool
    sections: List[object]
    total_pages: Optional[int]
    page_range: Optional[
        List[int]
    ]  # Only available if page_range is set in the request parameters.


class Vision(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, api_url, headers)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    def vocr(self, params: VOCRParams) -> OCRResponse: ...
    @overload
    def vocr(self, blob: bytes, options: VOCRParams = None) -> OCRResponse: ...

    def vocr(
        self,
        blob: Union[VOCRParams, bytes],
        options: VOCRParams = None,
    ) -> OCRResponse:
        path = "/vocr"
        options = options or {}
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = Request(
                config=self.config,
                path="/vocr",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = Request(
            config=self.config,
            path=path,
            params=options,
            files=files,
            verb="post",
        ).perform_with_content()
        return resp

    @overload
    def object_detection(self, params: ObjectDetectionParams) -> ObjectDetectionResponse: ...
    @overload
    def object_detection(
        self, blob: bytes, options: ObjectDetectionParams = None
    ) -> ObjectDetectionResponse: ...

    def object_detection(
        self,
        blob: Union[ObjectDetectionParams, bytes],
        options: ObjectDetectionParams = None,
    ) -> ObjectDetectionResponse:
        path = "/object_detection"
        options = options or {}
        if isinstance(blob, dict):
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp
        files = {"file": blob}
        resp = Request(
            config=self.config,
            path=path,
            params=options,
            files=files,
            verb="post",
        ).perform_with_content()
        return resp


class AsyncVision(ClientConfig):
    config: AsyncRequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, api_url, headers)
        self.config = AsyncRequestConfig(
            api_url=api_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    async def vocr(self, params: VOCRParams) -> OCRResponse: ...
    @overload
    async def vocr(self, blob: bytes, options: VOCRParams = None) -> OCRResponse: ...

    async def vocr(
        self,
        blob: Union[VOCRParams, bytes],
        options: VOCRParams = None,
    ) -> OCRResponse:
        path = "/vocr"
        options = options or {}
        if isinstance(blob, dict):
            resp = await AsyncRequest(
                headers=self.headers,
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = await AsyncRequest(
            headers=self.headers,
            config=self.config,
            path=path,
            params=options,
            files=files,
            verb="post",
        ).perform_with_content()
        return resp

    @overload
    async def object_detection(self, params: ObjectDetectionParams) -> ObjectDetectionResponse: ...
    @overload
    async def object_detection(
        self, blob: bytes, options: ObjectDetectionParams = None
    ) -> ObjectDetectionResponse: ...

    async def object_detection(
        self,
        blob: Union[ObjectDetectionParams, bytes],
        options: ObjectDetectionParams = None,
    ) -> ObjectDetectionResponse:
        path = "/object_detection"
        options = options or {}
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = await AsyncRequest(
                headers=self.headers,
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            files=files,
            verb="post",
        ).perform_with_content()
        return resp
