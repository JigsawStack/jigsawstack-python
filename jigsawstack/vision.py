from typing import Any, Dict, List, Union, cast, Optional
from typing_extensions import NotRequired, TypedDict, Literal
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict, Literal
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig


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


class ObjectDetectionResponse(TypedDict):
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

    def object_detection(self, params: ObjectDetectionParams) -> ObjectDetectionResponse:
        path = "/object_detection"
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

    async def object_detection(self, params: ObjectDetectionParams) -> ObjectDetectionResponse:
        path = "/object_detection"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
