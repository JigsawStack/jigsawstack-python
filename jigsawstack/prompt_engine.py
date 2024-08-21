from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
from typing import List, Union
from ._config import ClientConfig



class PromptEngineResult(TypedDict):
    prompt: str
    return_prompt:str
    id:str


class PromptEngineRunParams(TypedDict):
    input_values: object


class PromptEngineRunResponse(TypedDict):
    success: bool
    result:str

class PromptEngineCreateParams(TypedDict):
    prompt: str

    inputs: List[object]

    return_prompt: str 

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
    def create(self, params: PromptEngineCreateParams) -> PromptEngineCreateResponse:
        path = "/prompt_engine"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
        return resp
    
    def get(self, id:str) -> PromptEngineGetResponse:
        path = f"/prompt_engine/{id}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params={},verb="get").perform_with_content()
        return resp
    
    def list(self, params:PromptEngineListParams) -> PromptEngineListResponse:

        if params.get('limit') is None:
            params['limit'] = 20
        
        if params.get('page') is None:
            params['page'] = 1

        
        limit = params.get('limit')
        page = params.get('page')
    
        path = f"/prompt_engine?limit={limit}&page={page}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params={},verb="get").perform_with_content()
        return resp
    
    def delete(self, id:str) -> PromptEngineDeleteResponse:
        path = f"/prompt_engine/{id}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params={},verb="DELETE").perform_with_content()
        return resp
    
    def run(self, id:str, params:PromptEngineRunParams) -> PromptEngineRunResponse:
        path = f"/prompt_engine/{id}"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
        return resp