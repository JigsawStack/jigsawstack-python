from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict


class Spam(TypedDict):
    is_spam: bool
    score: float


class SpamCheckParams(TypedDict):
    text: str


class SpamCheckResponse(TypedDict):
    success: bool
    check: Spam


class SpellCheckParams(TypedDict):
    text: str
    language_code: str


class SpellCheckResponse(TypedDict):
    success: bool
    misspellings_found: int
    auto_correct_text: str


class ProfanityParams(TypedDict):
    text: str
    censor_replacement: NotRequired[str]


class ProfanityResponse(TypedDict):
    success: bool
    clean_text: str
    profanities: List[str]
    profanities_found: int


class NSFWParams(TypedDict):
    url: str


class NSFWResponse(TypedDict):
    success: bool


class EmailValidationParams(TypedDict):
    email: str


class EmailValidationResponse(TypedDict):
    success: bool
    email: str
    disposable: bool
    role_account: bool
    free: bool
    has_mx_records: bool
    username: bool
    domain: bool
    valid: bool


class Validate(ClientConfig):

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

    def email(self, params: EmailValidationParams) -> EmailValidationResponse:
        email = params.get("email")
        path = f"/validate/email?email={email}"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def nsfw(self, url: str) -> NSFWResponse:
        path = f"/validate/nsfw?url={url}"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params={"url": url}),
            verb="get",
        ).perform_with_content()
        return resp

    def profanity(self, params: ProfanityParams) -> ProfanityResponse:
        text = params.get("text")
        censor_replacement = params.get("censor_replacement", "*")
        path = (
            f"/validate/profanity?text={text}&censor_replacement={censor_replacement}"
        )
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def spellcheck(self, params: SpellCheckParams) -> SpellCheckResponse:
        text = params.get("text")
        language_code = params.get("language_code", "en")
        path = f"/validate/spell_check?text={text}&language_code={language_code}"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp

    def spamcheck(self, params: SpamCheckParams) -> SpamCheckResponse:
        path = "/ai/spamcheck"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
