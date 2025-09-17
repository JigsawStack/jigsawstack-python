import json
from typing import Any, Dict, Generator, Generic, List, TypedDict, Union, cast

import requests
from typing_extensions import Literal, TypeVar

from .exceptions import NoContentError, raise_for_code_and_type

RequestVerb = Literal["get", "post", "put", "patch", "delete"]

T = TypeVar("T")


class RequestConfig(TypedDict):
    base_url: str
    api_key: str
    headers: Union[Dict[str, str], None]


# This class wraps the HTTP request creation logic
class Request(Generic[T]):
    def __init__(
        self,
        config: RequestConfig,
        path: str,
        params: Union[Dict[Any, Any], List[Dict[Any, Any]]],
        verb: RequestVerb,
        data: Union[bytes, None] = None,
        stream: Union[bool, None] = False,
        files: Union[Dict[str, Any], None] = None,
    ):
        self.path = path
        self.params = params
        self.verb = verb
        self.base_url = config.get("base_url")
        self.api_key = config.get("api_key")
        self.data = data
        self.headers = config.get("headers", None) or {"Content-Type": "application/json"}
        self.stream = stream
        self.files = files

    def perform(self) -> Union[T, None]:
        """Is the main function that makes the HTTP request
        to the JigsawStack API. It uses the path, params, and verb attributes
        to make the request.

        Returns:
            Union[T, None]: A generic type of the Request class or None

        Raises:
            requests.HTTPError: If the request fails
        """
        resp = self.make_request(url=f"{self.base_url}{self.path}")

        # for binary responses
        if resp.status_code == 200:
            content_type = resp.headers.get("content-type", "")
            if not resp.text or any(
                t in content_type
                for t in ["audio/", "image/", "application/octet-stream", "image/png"]
            ):
                return cast(T, resp.content)

        # for json resposes.
        if resp.status_code != 200:
            try:
                error = resp.json()
                raise_for_code_and_type(
                    code=resp.status_code,
                    message=error.get("message"),
                    err=error.get("error"),
                )
            except json.JSONDecodeError:
                raise_for_code_and_type(
                    code=500,
                    message="Failed to parse response. Invalid content type or encoding.",
                )

        # For JSON responses
        try:
            return cast(T, resp.json())
        except json.JSONDecodeError:
            return cast(T, resp)

    def perform_file(self) -> Union[T, None]:
        resp = self.make_request(url=f"{self.base_url}{self.path}")

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

        # for binary responses
        if resp.status_code == 200:
            content_type = resp.headers.get("content-type", "")
            if "application/json" not in content_type:
                resp = cast(T, resp.content)
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
            "Accept": "application/json",
            "x-api-key": f"{self.api_key}",
        }

        # Only add Content-Type if not using multipart (files)
        if not self.files and not self.data:
            h["Content-Type"] = "application/json"

        _headers = h.copy()

        # Don't override Content-Type if using multipart
        if self.files and "Content-Type" in self.headers:
            self.headers.pop("Content-Type")

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
        resp = self.make_request(url=f"{self.base_url}{self.path}")

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
        files = self.files

        _requestParams = None
        _json = None
        _data = None
        _files = None

        if verb.lower() in ["get", "delete"]:
            _requestParams = params
        elif files:  # multipart request
            _files = files
            if params and isinstance(params, dict):
                _data = {"body": json.dumps(params)}
            headers.pop("Content-Type", None)  # let requests set it for multipart
        elif data:  # raw data request
            _data = data
        else:  # pure JSON request
            _json = params
        try:
            return requests.request(
                verb,
                url,
                params=_requestParams,
                json=_json,
                headers=headers,
                data=_data,
                files=_files,
                stream=self.stream,
            )
        except requests.HTTPError as e:
            raise e
