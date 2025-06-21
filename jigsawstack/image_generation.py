from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict, Literal, Required
from .request import Request, RequestConfig
from .async_request import AsyncRequest

from typing import List, Union
from ._config import ClientConfig

class AdvanceConfig(TypedDict):
    negative_prompt: NotRequired[str]
    guidance: NotRequired[int]
    seed: NotRequired[int]

class ImageGenerationParams(TypedDict):
    prompt: Required[str]
    """
    The text to generate the image from.
    """
    aspect_ratio: NotRequired[Literal["1:1", "16:9", "21:9", "3:2", "2:3", "4:5", "5:4", "3:4", "4:3", "9:16", "9:21"]]
    """
    The aspect ratio of the image. The default is 1:1.
    """
    width: NotRequired[int]
    """
    The width of the image. The default is 512.
    """
    height: NotRequired[int]
    """
    The height of the image. The default is 512.
    """
    steps: NotRequired[int]
    """
    The number of steps to generate the image.
    """
    output_format: NotRequired[Literal["png", "svg"]]
    """
    The output format of the generated image. Can be 'png' or 'svg'.
    """
    advance_config: NotRequired[AdvanceConfig]
    """
    The advance configuration for the image generation. The default is None.
    You can pass the following:
    - `negative_prompt`: The negative prompt for the image generation
    - `guidance`: The guidance scale for the image generation
    - `seed`: The seed for reproducible generation
    """
    url: NotRequired[str]
    """
    URL to use as image input.
    """
    file_store_key: NotRequired[str]
    """
    File store key to use as image input.
    """

    return_type: NotRequired[Literal["url", "binary", "base64"]]

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

    def image_generation(self, params: ImageGenerationParams) -> ImageGenerationResponse:
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

    async def image_generation(self, params: ImageGenerationParams) -> ImageGenerationResponse:
        path = "/ai/image_generation"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params), # type: ignore
            verb="post",
        ).perform()
        return resp
    


    