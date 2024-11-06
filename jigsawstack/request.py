from typing import Any, Dict, Generic, List, Union, cast, TypedDict, Generator
import requests
from typing_extensions import Literal, TypeVar
from .exceptions import NoContentError, raise_for_code_and_type
import json

RequestVerb = Literal["get", "post", "put", "patch", "delete"]

T = TypeVar("T")


class RequestConfig(TypedDict):
    api_url: str
    api_key: str
    disable_request_logging: Union[bool, None] = False


# This class wraps the HTTP request creation logic
class Request(Generic[T]):
    def __init__(
        self,
        config: RequestConfig,
        path: str,
        params: Union[Dict[Any, Any], List[Dict[Any, Any]]],
        verb: RequestVerb,
        headers: Dict[str, str] = {"Content-Type": "application/json"},
        data: Union[bytes, None] = None,
        stream: Union[bool, None] = False,
    ):
        self.path = path
        self.params = params
        self.verb = verb
        self.api_url = config.get("api_url")
        self.api_key = config.get("api_key")
        self.data = data
        self.headers = headers
        self.disable_request_logging = config.get("disable_request_logging")
        self.stream = stream

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
                message="Failed to parse JigsawStack API response. Please try again.",
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

        if (
            "application/json" not in resp.headers["content-type"]
            and resp.status_code != 200
        ):
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

        if self.disable_request_logging:
            h["x-jigsaw-no-request-log"] = "true"

        _headers = h.copy()
        _headers.update(self.headers)

        return _headers

    def perform_streaming(self) -> Generator[Union[T, str], None, None]:
        """Is the main function that makes the HTTP request
        to the JigsawStack API. It uses the path, params, and verb attributes
        to make the request.

        Returns:
            Generator[bytes, None, None]: A generator of bytes

        Raises:
            requests.HTTPError: If the request fails
        """
        resp = self.make_request(url=f"{self.api_url}{self.path}")

        # delete calls do not return a body
        if resp.text == "":
            return None

        if resp.status_code != 200:
            error = resp.json()
            raise_for_code_and_type(
                code=resp.status_code,
                message=error.get("message"),
                err=error.get("error"),
            )

        def try_parse_data(chunk: bytes) -> Union[T, str]:
            if not chunk:
                return chunk
            # Decode bytes to text
            text = chunk.decode("utf-8")

            try:
                # Try to parse as JSON
                return json.loads(text)
            except json.JSONDecodeError:
                # Return as text if not valid JSON
                return text

        # Yield content in chunks
        def chunk_generator():
            for chunk in resp.iter_content(chunk_size=1024):  # 1KB chunks
                if chunk:  # Filter out keep-alive new chunks
                    yield try_parse_data(chunk)

        return chunk_generator()

    def perform_with_content_streaming(self) -> Generator[Union[T, str], None, None]:
        """
        Perform an HTTP request and return the response content as a streaming response.

        Returns:
            T: The content of the response

        Raises:
            NoContentError: If the response content is `None`.
        """
        resp = self.perform_streaming()
        if resp is None:
            raise NoContentError()
        return resp

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
            return requests.request(
                verb,
                url,
                params=_requestParams,
                json=params,
                headers=headers,
                data=data,
                stream=self.stream,
            )
        except requests.HTTPError as e:
            raise e
