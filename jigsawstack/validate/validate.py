from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from ..request import Request
from ._validate import EmailValidationParams, EmailValidationResponse, NSFWParams, NSFWResponse, ProfanityParams, ProfanityResponse,SpellCheckParams, SpellCheckResponse, SpamCheckParams, SpamCheckResponse
from .._config import ClientConfig

class Validate(ClientConfig):

    def email(self, params: EmailValidationParams) -> EmailValidationResponse:
        email = params.get('email')
        path = f"/validate/email?email={email}"
        resp = Request(
            api_url=self.api_url,
            api_key=self.api_key,
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    
    def nsfw(self, params: NSFWParams) -> NSFWResponse:
        url = params.get("url")
        path = f"/validate/nsfw?url={url}"
        resp = Request(
             api_url=self.api_url,
            api_key=self.api_key,
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    

    def profanity(self, params: ProfanityParams) -> ProfanityResponse:
        text = params.get("text")
        censor_replacement = params.get("censor_replacement", "*")
        path = f"/validate/profanity?text={text}&censor_replacement={censor_replacement}"
        resp = Request(
            api_url=self.api_url,
            api_key=self.api_key,
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    

    def spell_check(self, params: SpellCheckParams) -> SpellCheckResponse:
        text = params.get("text")
        language_code = params.get("language_code","en")
        path = f"/validate/spell_check?text={text}&language_code={language_code}"
        resp = Request(
            api_url=self.api_url,
            api_key=self.api_key,
            path=path, params=cast(Dict[Any, Any], params), verb="get"
        ).perform_with_content()
        return resp
    def spam_check(self, params: SpamCheckParams) -> SpamCheckResponse:
        path = "/ai/spamcheck"
        resp = Request(
            api_url=self.api_url,
            api_key=self.api_key,
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp