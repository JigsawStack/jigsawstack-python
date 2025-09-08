from typing import Any, Dict, List, Union, cast, Optional, overload
from typing_extensions import NotRequired, TypedDict, Literal
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from .helpers import build_path
from ._types import BaseResponse


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

    @overload
    def vocr(self, params: VOCRParams) -> OCRResponse: ...
    @overload
    def vocr(self, blob: bytes, options: VOCRParams = None) -> OCRResponse: ...

    def vocr(
        self,
        blob: Union[VOCRParams, bytes],
        options: VOCRParams = None,
    ) -> OCRResponse:
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

        options = options or {}
        path = build_path(base_path="/vocr", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = Request(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
            verb="post",
        ).perform_with_content()
        return resp

    @overload
    def object_detection(
        self, params: ObjectDetectionParams
    ) -> ObjectDetectionResponse: ...
    @overload
    def object_detection(
        self, blob: bytes, options: ObjectDetectionParams = None
    ) -> ObjectDetectionResponse: ...

    def object_detection(
        self,
        blob: Union[ObjectDetectionParams, bytes],
        options: ObjectDetectionParams = None,
    ) -> ObjectDetectionResponse:
        if isinstance(blob, dict):
            resp = Request(
                config=self.config,
                path="/object_detection",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/object_detection", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = Request(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
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

    @overload
    async def vocr(self, params: VOCRParams) -> OCRResponse: ...
    @overload
    async def vocr(self, blob: bytes, options: VOCRParams = None) -> OCRResponse: ...

    async def vocr(
        self,
        blob: Union[VOCRParams, bytes],
        options: VOCRParams = None,
    ) -> OCRResponse:
        if isinstance(blob, dict):
            resp = await AsyncRequest(
                config=self.config,
                path="/vocr",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/vocr", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
            verb="post",
        ).perform_with_content()
        return resp

    @overload
    async def object_detection(
        self, params: ObjectDetectionParams
    ) -> ObjectDetectionResponse: ...
    @overload
    async def object_detection(
        self, blob: bytes, options: ObjectDetectionParams = None
    ) -> ObjectDetectionResponse: ...

    async def object_detection(
        self,
        blob: Union[ObjectDetectionParams, bytes],
        options: ObjectDetectionParams = None,
    ) -> ObjectDetectionResponse:
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = await AsyncRequest(
                config=self.config,
                path="/object_detection",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/object_detection", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
            verb="post",
        ).perform_with_content()
        return resp
