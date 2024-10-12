from typing import Any, Dict, List, cast, Union
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict


class TextToSpeechParams(TypedDict):
    text: str
    accent: NotRequired[str]
    speaker_clone_url: NotRequired[str]
    speaker_clone_file_store_key: NotRequired[str]


class TextToSpeechResponse(TypedDict):
    success: bool
    text: str
    chunks: List[object]


class SpeechToTextParams(TypedDict):
    url: str
    file_store_key: NotRequired[str]
    language: NotRequired[str]
    translate: NotRequired[bool]
    by_speaker: NotRequired[bool]
    webhook_url: NotRequired[str]
    batch_size: NotRequired[int]


class SpeechToTextResponse(TypedDict):
    success: bool
    text: str
    chunks: List[object]


class Audio(ClientConfig):
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

    def speech_to_text(self, params: SpeechToTextParams) -> SpeechToTextResponse:
        path = "/ai/transcribe"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def text_to_speech(self, params: TextToSpeechParams) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def speaker_voice_accents(self) -> TextToSpeechResponse:
        path = "/ai/tts"
        resp = Request(
            config=self.config,
            path=path,
            params={},
            verb="get",
        ).perform_with_content()
        return resp
