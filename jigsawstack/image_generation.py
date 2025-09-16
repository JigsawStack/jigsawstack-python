from typing import Any, Dict, Union, cast

from typing_extensions import Literal, NotRequired, Required, TypedDict

from ._config import ClientConfig
from .async_request import AsyncRequest
from .request import Request, RequestConfig


class AdvanceConfig(TypedDict):
    negative_prompt: NotRequired[str]
    guidance: NotRequired[int]
    seed: NotRequired[int]


class ImageGenerationParams(TypedDict):
    prompt: Required[str]
    """
    The text to generate the image from.
    """
    aspect_ratio: NotRequired[
        Literal[
            "1:1",
            "16:9",
            "21:9",
            "3:2",
            "2:3",
            "4:5",
            "5:4",
            "3:4",
            "4:3",
            "9:16",
            "9:21",
        ]
    ]
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
    url: NotRequired[str]
    """
    The generated image as a URL or base64 string.
    """


class ImageGeneration(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    def image_generation(
        self, params: ImageGenerationParams
    ) -> Union[ImageGenerationResponse, bytes]:
        path = "/ai/image_generation"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),  # type: ignore
            verb="post",
        ).perform()
        return resp


class AsyncImageGeneration(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    async def image_generation(
        self, params: ImageGenerationParams
    ) -> Union[ImageGenerationResponse, bytes]:
        path = "/ai/image_generation"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),  # type: ignore
            verb="post",
        ).perform()
        return resp
