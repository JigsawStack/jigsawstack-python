from typing import Any, Dict, List, Union, cast, overload
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict, Union, Optional
from .helpers import build_path


class Spam(TypedDict):
    is_spam: bool
    score: float


class SpamCheckParams(TypedDict):
    text: Union[str, List[str]]


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
    url: NotRequired[str]
    file_store_key: NotRequired[str]



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
        path = build_path(
            base_path="/validate/email",
            params=params,
        )

        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp
    
    def nsfw(self, params: Union[NSFWParams, bytes]) -> NSFWResponse:
        path="/validate/nsfw"
        if isinstance(params, dict):
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content()
            return resp

        _headers = {"Content-Type": "application/octet-stream"}
        resp = Request(
            config=self.config,
            path=path,
            params={}, #since we're already passing data.
            data=params,
            headers=_headers,
            verb="post",
        ).perform_with_content()
        return resp

    def profanity(self, params: ProfanityParams) -> ProfanityResponse:
        path = build_path(
            base_path="/validate/profanity",
            params=params,
        )
        resp = Request(
            config=self.config,
            path=path,
            params=cast(
                Dict[Any, Any], params
            ),
            verb="post",
        ).perform_with_content()
        return resp

    def spellcheck(self, params: SpellCheckParams) -> SpellCheckResponse:
        path = build_path(
            base_path="/validate/spell_check",
            params=params,
        )
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def spamcheck(self, params: SpamCheckParams) -> SpamCheckResponse:
        path = "/validate/spam_check"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp


class AsyncValidate(ClientConfig):

    config: AsyncRequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = AsyncRequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    async def email(self, params: EmailValidationParams) -> EmailValidationResponse:
        path = build_path(
            base_path="/validate/email",
            params=params,
        )
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="get",
        ).perform_with_content()
        return resp
    
    async def nsfw(self, params: Union[NSFWParams, bytes]) -> NSFWResponse:
        path="/validate/nsfw"
        if isinstance(params, dict):
            resp = await AsyncRequest(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content()
            return resp

        _headers = {"Content-Type": "application/octet-stream"}
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params={},
            data=params,
            headers=_headers,
            verb="post",
        ).perform_with_content()
        return resp

    async def profanity(self, params: ProfanityParams) -> ProfanityResponse:
        path = build_path(
            base_path="/validate/profanity",
            params=params,
        )
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(
                Dict[Any, Any], params
            ),
            verb="post",
        ).perform_with_content()
        return resp

    async def spellcheck(self, params: SpellCheckParams) -> SpellCheckResponse:
        path = build_path(
            base_path="/validate/spell_check",
            params=params,
        )
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    async def spamcheck(self, params: SpamCheckParams) -> SpamCheckResponse:
        path = "/validate/spam_check"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
