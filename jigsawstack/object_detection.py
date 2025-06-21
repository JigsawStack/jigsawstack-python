from typing import Any, Dict, List, Union, cast, Literal
from typing_extensions import NotRequired, TypedDict
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


class UsageStats(TypedDict):
    """
    Usage statistics - structure depends on the RunPod response
    """
    pass  # Flexible structure for usage stats


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
    
    _usage: NotRequired[UsageStats]
    """
    Optional usage statistics
    """


class ObjectDetection(ClientConfig):
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

    def detect(self, params: ObjectDetectionParams) -> ObjectDetectionResponse:
        """
        Detect objects and/or GUI elements in an image
        
        Args:
            params: Object detection parameters
            
        Returns:
            Object detection response with detected objects, GUI elements, and optional annotated image
        """
        resp = Request(
            config=self.config,
            path="/ai/object_detection",
            params=cast(Dict[Any, Any], params),
            verb="POST",
        ).perform_with_content()
        
        return resp


class AsyncObjectDetection(ClientConfig):
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

    async def detect(self, params: ObjectDetectionParams) -> ObjectDetectionResponse:
        """
        Detect objects and/or GUI elements in an image (async)
        
        Args:
            params: Object detection parameters
            
        Returns:
            Object detection response with detected objects, GUI elements, and optional annotated image
        """
        resp = await AsyncRequest(
            config=self.config,
            path="/ai/object_detection",
            params=cast(Dict[Any, Any], params),
            verb="POST",
        ).perform_with_content()
        
        return resp
