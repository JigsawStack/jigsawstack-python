from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from typing_extensions import NotRequired, TypedDict



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
    ai_overview:  NotRequired[bool]
    """
    Include AI powered overview in the search results. The default value is True
    """
    safe_search: NotRequired[str]
    """
    Include offensive results in the search results. The default value is "moderate". Supported values:  moderate, strict, off
    """
    spell_check: NotRequired[bool]
    """
    Spell check the search query.
    """


class Search:
    @classmethod
    def ai_search(params: AISearchParams) -> SearchAIResponse:
        path = "/web/search"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="post"
        ).perform_with_content()
        return resp
    

    @classmethod
    def suggestion(params: SearchSuggestionParams) -> SearchSuggestionResponse:
        path = "/web/search/suggest"
        resp = request.Request(
            path=path, params=cast(Dict[Any, Any], params), verb="patch"
        ).perform_with_content()
        return resp
