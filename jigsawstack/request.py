from typing import Any, Dict, Generic, List, Union, cast
import requests
from typing_extensions import Literal, TypeVar
from .exceptions import NoContentError, raise_for_code_and_type

RequestVerb = Literal["get", "post", "put", "patch", "delete"]

T = TypeVar("T")


# This class wraps the HTTP request creation logic
class Request(Generic[T]):
    def __init__(
        self,
        api_url:str,
        api_key:str,
        path: str,
        params: Union[Dict[Any, Any], List[Dict[Any, Any]]],
        verb: RequestVerb,
        headers: Dict[str, str] = {"Content-Type": "application/json"},
        data : Union[bytes, None] = None
    ):
        self.path = path
        self.params = params
        self.verb = verb
        self.api_url = api_url
        self.api_key = api_key
        self.data = data
        self.headers = headers

    def perform(self) -> Union[T, None]:
        """Is the main function that makes the HTTP request
        to the JigsawStack API. It uses the path, params, and verb attributes
        to make the request.

        Returns:
            Union[T, None]: A generic type of the Request class or None

        Raises:
            requests.HTTPError: If the request fails
        """
        resp = self.make_request(url=f"{self.api_url}{self.path}")

        # delete calls do not return a body
        if resp.text == "" and resp.status_code == 200:
            return None

        # this is a safety net, if we get here it means the JigsawStack API is having issues
        # and most likely the gateway is returning htmls
        if "application/json" not in resp.headers["content-type"]:
            raise_for_code_and_type(
                code=500,
                message="Failed to parse JigsawStack API response. Please try again."
            )

        # handle error in case there is a statusCode attr present
        # and status != 200 and response is a json.
        if resp.status_code != 200:
            error = resp.json()
            raise_for_code_and_type(
                code=resp.status_code,
                message=error.get("message"),
                err=error.get("error"),
            )
        
        return cast(T, resp.json())
    

    def perform_file(self) -> Union[T, None]:
    
        resp = self.make_request(url=f"{self.api_url}{self.path}")

        # delete calls do not return a body
        if resp.text == "" and resp.status_code == 200:
            return None
        # handle error in case there is a statusCode attr present
        # and status != 200 and response is a json.


        if "application/json" not in resp.headers["content-type"] and resp.status_code != 200:
         raise_for_code_and_type(
            code=500,
            message="Failed to parse JigsawStack API response. Please try again.",
            error_type="InternalServerError",
        )
         
        if resp.status_code != 200:
            error = resp.json()
            raise_for_code_and_type(
                code=resp.status_code,
                message=error.get("message"),
                err=error.get("error"),
            )
        return resp

    def perform_with_content(self) -> T:
        """
        Perform an HTTP request and return the response content.

        Returns:
            T: The content of the response

        Raises:
            NoContentError: If the response content is `None`.
        """
        resp = self.perform()
        if resp is None:
            raise NoContentError()
        return resp
    

    def perform_with_content_file(self) -> T:
        """
        Perform an HTTP request and return the response content.

        Returns:
            T: The content of the response

        Raises:
            NoContentError: If the response content is `None`.
        """
        resp = self.perform_file()
        if resp is None:
            raise NoContentError()
        return resp


    def __get_headers(self) -> Dict[Any, Any]:
        """get_headers returns the HTTP headers that will be
        used for every req.

        Returns:
            Dict: configured HTTP Headers
        """

        h = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": f"{self.api_key}",
        }
        _headers = h.copy()
        _headers.update(self.headers)

        return _headers
    

    def make_request(self, url: str) -> requests.Response:
        """make_request is a helper function that makes the actual
        HTTP request to the JigsawStack API.

        Args:
            url (str): The URL to make the request to

        Returns:
            requests.Response: The response object from the request

        Raises:
            requests.HTTPError: If the request fails
        """
        headers = self.__get_headers()
        params = self.params
        verb = self.verb
        data = self.data

        _requestParams = None

        if verb.lower() in ["get", "delete"]:
            _requestParams = params

        try:
            return requests.request(verb, url, params=_requestParams, json=params,headers=headers, data=data)
        except requests.HTTPError as e:
            raise e