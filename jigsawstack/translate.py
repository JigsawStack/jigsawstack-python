from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from typing import List, Union
from ._config import ClientConfig


class TranslateParams(TypedDict):
    target_language: str
    """
    Target langauge to translate to.
    """
    current_language: str
    """
    Language to translate from.
    """
    text: str
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

    def translate(self, params: TranslateParams) -> TranslateResponse:
        path = "/ai/translate"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
