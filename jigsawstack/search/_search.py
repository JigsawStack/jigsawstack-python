from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from typing_extensions import NotRequired, TypedDict
from .._config import ClientConfig


class SearchAIResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    results : List[Any]

    is_safe : bool

    ai_overview : str

    spell_fixed:str

class SearchSuggestionResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """


    suggestions : List[str]



class SearchSuggestionParams(TypedDict):
    query: str
    """
    The search value. The maximum query character length is 200.
    """

class AISearchParams(TypedDict):
    query: str
    """
    The search value. The maximum query character length is 200.
    """
    ai_overview:  NotRequired[bool] = True
    """
    Include AI powered overview in the search results. The default value is True
    """
    safe_search: NotRequired[str] = "moderate"
    """
    Include offensive results in the search results. The default value is "moderate". Supported values:  moderate, strict, off
    """
    spell_check: NotRequired[bool] = True
    """
    Spell check the search query.
    """


class Search(ClientConfig):
    def ai_search(self,params: AISearchParams) -> SearchAIResponse:
        query = params["query"]
        ai_overview = params.get("ai_overview", "True")
        safe_search = params.get("safe_search","moderate")
        spell_check = params.get("spell_check", "True")
        path = f"/web/search?query={query}&ai_overview={ai_overview}&safe_search={safe_search}&spell_check={spell_check}"
        resp = request.Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="GET"
        ).perform_with_content()

        print(resp)
        return resp
    

    def suggestion(self, params: SearchSuggestionParams) -> SearchSuggestionResponse:
        query = params["query"]
        path = f"/web/search/suggest?query={query}"
        resp = request.Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path, params=cast(Dict[Any, Any], params), verb="GET"
        ).perform_with_content()

        print(resp)
        return resp
