from typing import Any, Dict, List, Union, cast, overload

from typing_extensions import NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest, AsyncRequestConfig
from .helpers import build_path
from .request import Request, RequestConfig


class Spam(TypedDict):
    is_spam: bool
    score: float


class SpamCheckParams(TypedDict):
    text: Union[str, List[str]]


class SpamCheckResponse(BaseResponse):
    check: Union[Spam, List[Spam]]


class SpellCheckParams(TypedDict):
    text: str
    language_code: NotRequired[str]


class Misspelling(TypedDict):
    word: Union[str, None]
    startIndex: int
    endIndex: int
    expected: List[str]
    auto_corrected: bool


class SpellCheckResponse(BaseResponse):
    misspellings_found: bool
    misspellings: List[Misspelling]
    auto_correct_text: str


class ProfanityParams(TypedDict):
    text: str
    censor_replacement: NotRequired[str]


class Profanity(TypedDict):
    profanity: Union[str, None]
    startIndex: int
    endIndex: int


class ProfanityResponse(BaseResponse):
    message: str
    clean_text: str
    profanities: List[Profanity]
    profanities_found: bool


class NSFWParams(TypedDict):
    url: NotRequired[str]
    file_store_key: NotRequired[str]


class NSFWResponse(BaseResponse):
    nsfw: bool
    nudity: bool
    gore: bool
    nsfw_score: float
    nudity_score: float
    gore_score: float


class Validate(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    def nsfw(self, params: NSFWParams) -> NSFWResponse: ...
    @overload
    def nsfw(self, blob: bytes, options: NSFWParams = None) -> NSFWResponse: ...

    def nsfw(
        self,
        blob: Union[NSFWParams, bytes],
        options: NSFWParams = None,
    ) -> NSFWResponse:
        path = "/validate/nsfw"
        options = options or {}
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = Request(
                config=self.config,
                path="/validate/nsfw",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = Request(
            config=self.config,
            path=path,
            params=options,
            files=files,
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
            params=cast(Dict[Any, Any], params),
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
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = AsyncRequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    @overload
    async def nsfw(self, params: NSFWParams) -> NSFWResponse: ...
    @overload
    async def nsfw(self, blob: bytes, options: NSFWParams = None) -> NSFWResponse: ...

    async def nsfw(
        self,
        blob: Union[NSFWParams, bytes],
        options: NSFWParams = None,
    ) -> NSFWResponse:
        path = "/validate/nsfw"
        options = options or {}
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = await AsyncRequest(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        files = {"file": blob}
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            files=files,
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
            params=cast(Dict[Any, Any], params),
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
