
from typing import Any, Dict, List, cast
from typing_extensions import NotRequired, TypedDict




class Spam(TypedDict):
      is_spam : bool
      score : float


class SpamCheckParams(TypedDict):
        text: str
        
class SpamCheckResponse(TypedDict):
        success: bool
        check : Spam


class SpellCheckParams(TypedDict):
        text: str
        language_code :str

class SpellCheckResponse(TypedDict):
        success: bool
        misspellings_found: int
        auto_correct_text :str

class ProfanityParams(TypedDict):
    text: str
    censor_replacement : NotRequired[str]

class ProfanityResponse(TypedDict):
    success: bool
    clean_text : str
    profanities : List[str]
    profanities_found : int

class NSFWParams(TypedDict):
    url : str

class NSFWResponse(TypedDict):
    success : bool

class EmailValidationParams(TypedDict):
    email:str

class EmailValidationResponse(TypedDict):
    success:bool
    email : str
    disposable :bool
    role_account : bool
    free :  bool
    has_mx_records : bool
    username :  bool
    domain : bool
    valid :   bool