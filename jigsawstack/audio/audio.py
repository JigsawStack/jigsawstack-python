from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._audio import SpeechToTextParams, SpeechToTextResponse

class Audio:
    @classmethod
    def speech_to_text(cls, params: SpeechToTextParams) -> SpeechToTextResponse:
        path = "/ai/transcribe"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp