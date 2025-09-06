from typing import Any, Dict, List, Union, cast, overload
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict, Union, Optional
from .helpers import build_path
from ._types import BaseResponse


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
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
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

        options = options or {}
        path = build_path(base_path="/validate/nsfw", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = Request(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
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
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = AsyncRequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
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
        if isinstance(
            blob, dict
        ):  # If params is provided as a dict, we assume it's the first argument
            resp = await AsyncRequest(
                config=self.config,
                path="/validate/nsfw",
                params=cast(Dict[Any, Any], blob),
                verb="post",
            ).perform_with_content()
            return resp

        options = options or {}
        path = build_path(base_path="/validate/nsfw", params=options)
        content_type = options.get("content_type", "application/octet-stream")
        headers = {"Content-Type": content_type}

        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=options,
            data=blob,
            headers=headers,
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
