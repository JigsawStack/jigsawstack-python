from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict, Literal
from .request import Request, RequestConfig
from .async_request import AsyncRequest

from typing import List, Union
from ._config import ClientConfig

class ImageGenerationparams(TypedDict):
    prompt: str
    """"
    The text to generate the image from."
    """
    aspect_ratio: Literal["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "3:4", "4:3", "9:16", "9:21"]
    """
    The aspect ratio of the image. The default is 1:1.
    """
    width: NotRequired[int]
    """"
    The width of the image. The default is 512."
    """
    height: NotRequired[int]
    """
    The height of the image. The default is 512."
    """
    steps: NotRequired[int]
    """"
    The number of steps to generate the image.""
    """
    advance_config: NotRequired[Dict[str, Union[int, str]]]
    """
    The advance configuration for the image generation. The default is None.
    You can pass the following:
    - `seed`: The seed for the image generation. The default is None.
    - `guidance`: The guidance for the image generation. The default is None.
    - `negative_prompt`: The negative prompt for the image generation. The default is None.
    """

class ImageGenerationResponse(TypedDict):
    success: bool
    """
    Indicates whether the image generation was successful.
    """
    image: bytes
    """
    The generated image as a blob.
    """

class ImageGeneration(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging=disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    def image_generation(self, params: ImageGenerationparams) -> ImageGenerationResponse:
        path = "/ai/image_generation"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params), # type: ignore
            verb="post",
        ).perform()
        return resp
    
class AsyncImageGeneration(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging=disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    async def image_generation(self, params: ImageGenerationparams) -> ImageGenerationResponse:
        path = "/ai/image_generation"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params), # type: ignore
            verb="post",
        ).perform()
        return resp
    


    