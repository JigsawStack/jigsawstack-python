from typing import Any, Dict, List, Union, cast, overload

from typing_extensions import Literal, NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest
from .helpers import build_path
from .request import Request, RequestConfig


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
    """
    The return type of the response.
    """


class TranslateParams(TypedDict):
    target_language: str
    """
    Target langauge to translate to.
    """
    current_language: NotRequired[str]
    """
    Language to translate from.
    """
    text: Union[str, List[str]]
    """
    The text to translate.
    """


class TranslateResponse(BaseResponse):
    translated_text: Union[str, List[str]]
    """
    The translated text.
    """


class TranslateImageResponse(BaseResponse):
    url: str
    """
    The URL or base64 of the translated image.
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

    def text(self, params: TranslateParams) -> TranslateResponse:
        resp = Request(
            config=self.config,
            path="/ai/translate",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp

    @overload
    def image(self, params: TranslateImageParams) -> Union[TranslateImageResponse, bytes]: ...
    @overload
    def image(
        self, blob: bytes, options: TranslateImageParams = None
    ) -> Union[TranslateImageResponse, bytes]: ...

    def image(
        self,
        blob: Union[TranslateImageParams, bytes],
        options: TranslateImageParams = None,
    ) -> Union[TranslateImageResponse, bytes]:
        path = "/ai/translate/image"
        options = options or {}
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = Request(
                config=self.config,
                path="/ai/translate/image",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        
        files = {"file": blob}
        resp = Request(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            files=files,
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

    async def text(self, params: TranslateParams) -> TranslateResponse:
        resp = await AsyncRequest(
            config=self.config,
            path="/ai/translate",
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform()
        return resp

    @overload
    async def image(self, params: TranslateImageParams) -> Union[TranslateImageResponse, bytes]: ...
    @overload
    async def image(
        self, blob: bytes, options: TranslateImageParams = None
    ) -> Union[TranslateImageResponse, bytes]: ...

    async def image(
        self,
        blob: Union[TranslateImageParams, bytes],
        options: TranslateImageParams = None,
    ) -> Union[TranslateImageResponse, bytes]:
        path = "/ai/translate/image"
        options = options or {}
        if isinstance(blob, dict):
            resp = await AsyncRequest(
                config=self.config,
                path="/ai/translate/image",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            files=files,
            verb="post",
        ).perform_with_content()
        return resp
