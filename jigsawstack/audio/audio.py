from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._audio import SpeechToTextParams, SpeechToTextResponse
from .._config import ClientConfig
class Audio(ClientConfig):

    def speech_to_text(self, params: SpeechToTextParams) -> SpeechToTextResponse:
        path = "/ai/transcribe"
        resp = request.Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp