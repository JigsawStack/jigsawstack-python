from typing import Any, Dict, List, Union, cast, Generator
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from typing import List, Union
from ._config import ClientConfig


class PromptEngineResult(TypedDict):
    prompt: str
    return_prompt: str
    id: str


class PromptEngineRunParams(TypedDict):
    prompt: str
    inputs: NotRequired[List[object]]
    return_prompt: Union[str, List[object], Dict[str, str]]
    input_values: NotRequired[Dict[str, str]]
    stream: Union[bool, None] = False
    use_internet: Union[bool, None] = False


class PromptEngineExecuteParams(TypedDict):
    id: str
    input_values: object
    stream: Union[bool, None] = False


class PromptEngineRunResponse(TypedDict):
    success: bool
    result: Any


class PromptEngineCreateParams(TypedDict):
    prompt: str
    inputs: NotRequired[List[object]]
    return_prompt: Union[str, List[object], Dict[str, str]]
    use_internet: Union[bool, None] = False
    optimize_prompt: Union[bool, None] = False


class PromptEngineCreateResponse(TypedDict):
    success: bool
    prompt_engine_id: str


class PromptEngineGetResponse(PromptEngineResult):
    success: bool


class PromptEngineListResponse(TypedDict):
    success: bool
    prompt_engines: List[PromptEngineResult]


class PromptEngineListParams(TypedDict):
    limit: str
    page: str


class PromptEngineDeleteResponse(TypedDict):
    prompt_engine_id: str


class PromptEngine(ClientConfig):

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

    def create(self, params: PromptEngineCreateParams) -> PromptEngineCreateResponse:
        path = "/prompt_engine"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def get(self, id: str) -> PromptEngineGetResponse:
        path = f"/prompt_engine/{id}"
        resp = Request(
            config=self.config, path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    def list(
        self, params: Union[PromptEngineListParams, None] = None
    ) -> PromptEngineListResponse:

        if params is None:
            params = {}

        # Default limit and page to 20 and 1 respectively
        if params.get("limit") is None:
            params["limit"] = 20

        if params.get("page") is None:
            params["page"] = 0

        limit = params.get("limit")
        page = params.get("page")

        path = f"/prompt_engine?limit={limit}&page={page}"
        resp = Request(
            config=self.config, path=path, params={}, verb="get"
        ).perform_with_content()
        return resp

    def delete(self, id: str) -> PromptEngineDeleteResponse:
        path = f"/prompt_engine/{id}"
        resp = Request(
            config=self.config,
            path=path,
            params={},
            verb="DELETE",
        ).perform_with_content()
        return resp

    def run_prompt_direct(
        self, params: PromptEngineRunParams
    ) -> Union[PromptEngineRunResponse, Generator[Any, None, None]]:
        path = "/prompt_engine/run"
        stream = params.get("stream")
        if stream:
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content_streaming()
            return resp

        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def run(
        self, params: PromptEngineExecuteParams
    ) -> Union[PromptEngineRunResponse, Generator[Any, None, None]]:
        id = params.get("id")
        path = f"/prompt_engine/{id}"
        stream = params.get("stream")

        if stream:
            resp = Request(
                config=self.config,
                path=path,
                params=cast(Dict[Any, Any], params),
                verb="post",
            ).perform_with_content_streaming()
            return resp

        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
