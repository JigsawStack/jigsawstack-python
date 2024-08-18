from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
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
    def translate(self, params: TranslateParams) -> TranslateResponse:
        path = "/ai/translate"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
        return resp