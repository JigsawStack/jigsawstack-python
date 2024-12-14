from typing import Any, Dict, Generic, List, Union, cast, TypedDict, AsyncGenerator
import aiohttp
from typing_extensions import Literal, TypeVar
from .exceptions import NoContentError, raise_for_code_and_type
import json

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

    async def perform(self) -> Union[T, None]:
        """
        Async method to make an HTTP request to the JigsawStack API.

        Returns:
            Union[T, None]: A generic type of the Request class or None

        Raises:
            aiohttp.ClientResponseError: If the request fails
        """
        async with self.__get_session() as session:
            resp = await self.make_request(session, url=f"{self.api_url}{self.path}")

            # delete calls do not return a body
            if await resp.text() == "" and resp.status == 200:
                return None

            # safety net for non-JSON responses
            content_type = resp.headers.get("content-type", "")
            if "application/json" not in content_type:
                raise_for_code_and_type(
                    code=500,
                    message="Failed to parse JigsawStack API response. Please try again.",
                )

            # handle error responses
            if resp.status != 200:
                error = await resp.json()
                raise_for_code_and_type(
                    code=resp.status,
                    message=error.get("message"),
                    err=error.get("error"),
                )

            return cast(T, await resp.json())

    async def perform_file(self) -> Union[aiohttp.ClientResponse, None]:
        """
        Async method to make an HTTP request and return the raw response.

        Returns:
            Union[aiohttp.ClientResponse, None]: The raw response object
        """
        async with self.__get_session() as session:
            resp = await self.make_request(session, url=f"{self.api_url}{self.path}")

            # delete calls do not return a body
            if await resp.text() == "" and resp.status == 200:
                return None

            # handle error responses
            if (
                "application/json" not in resp.headers.get("content-type", "")
                and resp.status != 200
            ):
                raise_for_code_and_type(
                    code=500,
                    message="Failed to parse JigsawStack API response. Please try again.",
                    error_type="InternalServerError",
                )

            if resp.status != 200:
                error = await resp.json()
                raise_for_code_and_type(
                    code=resp.status,
                    message=error.get("message"),
                    err=error.get("error"),
                )
            return resp

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
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": f"{self.api_key}",
        }

        if self.disable_request_logging:
            h["x-jigsaw-no-request-log"] = "true"

        _headers = h.copy()
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
        """
        Make the actual async HTTP request.

        Args:
            session (aiohttp.ClientSession): The client session
            url (str): The URL to make the request to

        Returns:
            aiohttp.ClientResponse: The response object from the request
        """
        headers = self.__get_headers()
        params = self.params
        verb = self.verb
        data = self.data

        request_params = None if verb.lower() not in ["get", "delete"] else params

        try:
            return await session.request(
                verb,
                url,
                params=request_params,
                json=params,
                headers=headers,
                data=data,
            )
        except aiohttp.ClientError as e:
            raise e

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
