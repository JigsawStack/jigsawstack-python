import json
from typing import Any, AsyncGenerator, Dict, Generic, List, TypedDict, Union, cast
from io import BytesIO
import aiohttp
from typing_extensions import Literal, TypeVar

from .exceptions import NoContentError, raise_for_code_and_type

RequestVerb = Literal["get", "post", "put", "patch", "delete"]

T = TypeVar("T")


class AsyncRequestConfig(TypedDict):
    api_url: str
    api_key: str
    disable_request_logging: Union[bool, None] = False


class AsyncRequest(Generic[T]):
    def __init__(
        self,
        config: AsyncRequestConfig,
        path: str,
        params: Union[Dict[Any, Any], List[Dict[Any, Any]]],
        verb: RequestVerb,
        headers: Dict[str, str] = None,
        data: Union[bytes, None] = None,
        stream: Union[bool, None] = False,
        files: Union[Dict[str, Any], None] = None,  # Add files parameter
    ):
        self.path = path
        self.params = params
        self.verb = verb
        self.api_url = config.get("api_url")
        self.api_key = config.get("api_key")
        self.data = data
        self.headers = headers or {"Content-Type": "application/json"}
        self.disable_request_logging = config.get("disable_request_logging")
        self.stream = stream
        self.files = files  # Store files for multipart requests

    def __convert_params(
        self, params: Union[Dict[Any, Any], List[Dict[Any, Any]]]
    ) -> Dict[str, str]:
        """
        Convert parameters to string values for URL encoding.
        """
        if params is None:
            return {}

        if isinstance(params, str):
            return params

        if isinstance(params, list):
            return {}  # List params are only used in JSON body

        converted = {}
        for key, value in params.items():
            if isinstance(value, bool):
                converted[key] = str(value).lower()
            else:
                converted[key] = str(value)
        return converted

    async def perform(self) -> Union[T, None]:
        """
        Async method to make an HTTP request to the JigsawStack API.
        """
        async with self.__get_session() as session:
            resp = await self.make_request(session, url=f"{self.api_url}{self.path}")

            # For binary responses
            if resp.status == 200:
                content_type = resp.headers.get("content-type", "")
                if not resp.text or any(
                    t in content_type
                    for t in [
                        "audio/",
                        "image/",
                        "application/octet-stream",
                        "image/png",
                    ]
                ):
                    content = await resp.read()
                    return cast(T, content)

            # For error responses
            if resp.status != 200:
                try:
                    error = await resp.json()
                    raise_for_code_and_type(
                        code=resp.status,
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
                return cast(T, await resp.json())
            except json.JSONDecodeError:
                content = await resp.read()
                return cast(T, content)

    async def perform_file(self) -> Union[T, None]:
        async with self.__get_session() as session:
            resp = await self.make_request(session, url=f"{self.api_url}{self.path}")

            if resp.status != 200:
                try:
                    error = await resp.json()
                    raise_for_code_and_type(
                        code=resp.status,
                        message=error.get("message"),
                        err=error.get("error"),
                    )
                except json.JSONDecodeError:
                    raise_for_code_and_type(
                        code=500,
                        message="Failed to parse response. Invalid content type or encoding.",
                    )

            # For binary responses
            if resp.status == 200:
                content_type = resp.headers.get("content-type", "")
                if "application/json" not in content_type:
                    content = await resp.read()
                    return cast(T, content)

            return cast(T, await resp.json())

    async def perform_with_content(self) -> T:
        """
        Perform an async HTTP request and return the response content.

        Returns:
            T: The content of the response

        Raises:
            NoContentError: If the response content is `None`.
        """
        resp = await self.perform()
        if resp is None:
            raise NoContentError()
        return resp

    async def perform_with_content_file(self) -> Union[aiohttp.ClientResponse, None]:
        """
        Perform an async HTTP request and return the raw response.

        Returns:
            Union[aiohttp.ClientResponse, None]: The raw response

        Raises:
            NoContentError: If the response content is `None`.
        """
        resp = await self.perform_file()
        if resp is None:
            raise NoContentError()
        return resp

    def __get_headers(self) -> Dict[str, str]:
        """
        Prepare HTTP headers for the request.

        Returns:
            Dict[str, str]: Configured HTTP Headers
        """
        h = {
            "Accept": "application/json",
            "x-api-key": f"{self.api_key}",
        }

        # only add Content-Type if not using multipart (files)
        if not self.files and not self.data:
            h["Content-Type"] = "application/json"

        if self.disable_request_logging:
            h["x-jigsaw-no-request-log"] = "true"

        _headers = h.copy()

        # don't override Content-Type if using multipart
        if self.files and "Content-Type" in self.headers:
            self.headers.pop("Content-Type")

        _headers.update(self.headers)

        return _headers

    async def perform_streaming(self) -> AsyncGenerator[Union[T, str], None]:
        """
        Async method to stream response from JigsawStack API.

        Returns:
            AsyncGenerator[Union[T, str], None]: A generator of response chunks
        """
        async with self.__get_session() as session:
            resp = await self.make_request(session, url=f"{self.api_url}{self.path}")

            # delete calls do not return a body
            if await resp.text() == "":
                return

            if resp.status != 200:
                error = await resp.json()
                raise_for_code_and_type(
                    code=resp.status,
                    message=error.get("message"),
                    err=error.get("error"),
                )

            async for chunk in resp.content.iter_chunked(1024):  # 1KB chunks
                if chunk:
                    yield await self.__try_parse_data(chunk)

    async def perform_with_content_streaming(
        self,
    ) -> AsyncGenerator[Union[T, str], None]:
        """
        Perform an async HTTP request and return the response content as a streaming response.

        Returns:
            AsyncGenerator[Union[T, str], None]: Streaming response content

        Raises:
            NoContentError: If the response content is `None`.
        """
        resp = await self.perform_streaming()
        if resp is None:
            raise NoContentError()
        return resp

    async def make_request(
        self, session: aiohttp.ClientSession, url: str
    ) -> aiohttp.ClientResponse:
        headers = self.__get_headers()
        params = self.params
        verb = self.verb
        data = self.data
        files = self.files

        _params = None
        _json = None
        _data = None
        _form_data = None

        if verb.lower() in ["get", "delete"]:
            # convert params for URL encoding if needed
            _params = self.__convert_params(params)
        elif files:
            # for multipart requests - matches request.py behavior
            _form_data = aiohttp.FormData()

            # add file(s) to form data
            for field_name, file_data in files.items():
                if isinstance(file_data, bytes):
                    # just pass the blob without filename
                    _form_data.add_field(
                        field_name, BytesIO(file_data), content_type="application/octet-stream"
                    )
                elif isinstance(file_data, tuple):
                    # if tuple format (filename, data, content_type)
                    filename, content, content_type = file_data
                    _form_data.add_field(
                        field_name, content, filename=filename, content_type=content_type
                    )

            # add params as 'body' field in multipart form (JSON stringified)
            if params and isinstance(params, dict):
                _form_data.add_field("body", json.dumps(params), content_type="application/json")
        elif data:
            # for binary data without multipart
            _data = data
            # pass params as query parameters for binary uploads
            if params and isinstance(params, dict):
                _params = self.__convert_params(params)
        else:
            # for JSON requests
            _json = params

        # m,ake the request based on the data type
        if _form_data:
            return await session.request(
                verb,
                url,
                params=_params,
                data=_form_data,
                headers=headers,
            )
        elif _json is not None:
            return await session.request(
                verb,
                url,
                params=_params,
                json=_json,
                headers=headers,
            )
        else:
            return await session.request(
                verb,
                url,
                params=_params,
                data=_data,
                headers=headers,
            )

    def __get_session(self) -> aiohttp.ClientSession:
        """
        Create and return an async client session.

        Returns:
            aiohttp.ClientSession: An async client session
        """
        return aiohttp.ClientSession()

    @staticmethod
    async def __try_parse_data(chunk: bytes) -> Union[T, str]:
        """
        Attempt to parse a chunk of data as JSON or return as text.

        Args:
            chunk (bytes): The data chunk to parse

        Returns:
            Union[T, str]: Parsed JSON or raw text
        """
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
