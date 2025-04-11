from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest
from typing import List, Union
from ._config import ClientConfig


class TranslateImageParams(TypedDict):
    target_language: str
    """
    Target langauge to translate to.
    """
    url: str
    """
    The URL of the image to translate.
    """
    file_store_key: NotRequired[str]
    """
    The file store key of the image to translate.
    """

class TranslateParams(TypedDict):
    target_language: str
    """
    Target langauge to translate to.
    """
    current_language: str
    """
    Language to translate from.
    """
    text: Union[str, List[str]]
    """
    The text to translate.
    """

class TranslateResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    translated_text: str
    """
    The translated text.
    """

class TranslateImageResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    image: bytes
    """
    The image data that was translated.
    """

class TranslateListResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    translated_text: List[str]
    """
    The translated text.
    """


class Translate(ClientConfig):

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

    def translate_text(
        self, params: TranslateParams
    ) -> Union[TranslateResponse, TranslateListResponse]:
        resp = Request(
            config=self.config,
            path="/ai/translate",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp

    def translate_image(
    self, params: TranslateImageParams
) -> TranslateImageResponse:
        resp = Request(
            config=self.config,
            path="/ai/translate/image",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp

    def translate(
    self, params: Union[TranslateParams, TranslateImageParams]
) -> Union[TranslateResponse, TranslateListResponse, TranslateImageResponse]:
        if "url" in params or "file_store_key" in params:
            return self.translate_image(params)
        return self.translate_text(params)


class AsyncTranslate(ClientConfig):
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

    async def translate_text(
        self, params: TranslateParams
    ) -> Union[TranslateResponse, TranslateListResponse]:
        resp = await AsyncRequest(
            config=self.config,
            path="/ai/translate",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp

    async def translate_image(
        self, params: TranslateImageParams
    ) -> TranslateImageResponse:
        resp = await AsyncRequest(
            config=self.config,
            path="/ai/translate/image",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp

    async def translate(
        self, params: Union[TranslateParams, TranslateImageParams]
    ) -> Union[TranslateResponse, TranslateListResponse, TranslateImageResponse]:
        if "url" in params or "file_store_key" in params:
            return await self.translate_image(params)
        return await self.translate_text(params)
