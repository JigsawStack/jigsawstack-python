from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict


class TextToSpeechParams(TypedDict):
    text:str
    accent: NotRequired[str]
    speaker_clone_url: NotRequired[str]
    speaker_clone_file_store_key: NotRequired[str]

class TextToSpeechResponse(TypedDict):
    success:bool
    text: str
    chunks : List[object]

class SpeechToTextParams(TypedDict):
    url:str
    file_store_key : NotRequired[str]
    language : NotRequired[str]
    translate : NotRequired[bool]
    by_speaker : NotRequired[bool]
    webhook_url : NotRequired[str]

class SpeechToTextResponse(TypedDict):
    success:bool
    text : str
    chunks : List[object]


class Audio(ClientConfig):
    def speech_to_text(self, params: SpeechToTextParams) -> SpeechToTextResponse:
        path = "/ai/transcribe"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    
    def text_to_speech(self, params: TextToSpeechParams) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    def speaker_voice_accents(self) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params={}, verb="get"
        ).perform_with_content()
        return resp