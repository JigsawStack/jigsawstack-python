from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from ._validate import EmailValidationParams, EmailValidationResponse, NSFWParams, NSFWResponse, ProfanityParams, ProfanityResponse,SpellCheckParams, SpellCheckResponse, SpamCheckParams, SpamCheckResponse

class Validate:
    @classmethod
    def email(cls, params: EmailValidationParams) -> EmailValidationResponse:
        path = "/validate/email"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    
    @classmethod
    def nsfw(cls, params: NSFWParams) -> NSFWResponse:
        path = "/validate/nsfw"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    
    @classmethod
    def profanity(cls, params: ProfanityParams) -> ProfanityResponse:
        path = "/validate/profanity"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    
    @classmethod
    def spell_check(cls, params: SpellCheckParams) -> SpellCheckResponse:
        path = "/validate/spell_check"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    @classmethod
    def spam_check(cls, params: SpamCheckParams) -> SpamCheckResponse:
        path = "/ai/spamcheck"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp