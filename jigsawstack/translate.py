from typing import Any, Dict, List, Union, cast, overload
from typing_extensions import NotRequired, TypedDict, Literal
from .request import Request, RequestConfig
from .async_request import AsyncRequest
from typing import List, Union
from ._config import ClientConfig
from .helpers import build_path

class TranslateImageParams(TypedDict):
    target_language: str
    """
    Target langauge to translate to.
    """
    url: NotRequired[str]
    """
    The URL of the image to translate.
    """
    file_store_key: NotRequired[str]
    """
    The file store key of the image to translate.
    """

    return_type: NotRequired[Literal["url", "binary", "base64"]]

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

    def text(
        self, params: TranslateParams
    ) -> Union[TranslateResponse, TranslateListResponse]:
        resp = Request(
            config=self.config,
            path="/ai/translate",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp
    
    @overload
    def image(self, params: TranslateImageParams) -> TranslateImageResponse: ...
    @overload
    def image(self, file: bytes, options: TranslateImageParams = None) -> TranslateImageParams: ...

    def image(
        self,
        blob: Union[TranslateImageParams, bytes],
        options: TranslateImageParams = None,
    ) -> TranslateImageResponse:
        if isinstance(blob, dict): # If params is provided as a dict, we assume it's the first argument
            resp = Request(
                config=self.config,
                path="/ai/translate/image",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/ai/translate/image", params=options)
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

    async def text(
        self, params: TranslateParams
    ) -> Union[TranslateResponse, TranslateListResponse]:
        resp = await AsyncRequest(
            config=self.config,
            path="/ai/translate",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp
    
    @overload
    async def image(self, params: TranslateImageParams) -> TranslateImageResponse: ...
    @overload
    async def image(self, file: bytes, options: TranslateImageParams = None) -> TranslateImageParams: ...
    
    async def image(
        self,
        blob: Union[TranslateImageParams, bytes],
        options: TranslateImageParams = None,
    ) -> TranslateImageResponse:
        if isinstance(blob, dict):
            resp = await AsyncRequest(
                config=self.config,
                path="/ai/translate/image",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/ai/translate/image", params=options)
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