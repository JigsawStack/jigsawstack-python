import json
from io import BytesIO
from typing import Any, AsyncGenerator, Dict, Generic, List, Optional, TypedDict, Union, cast

import aiohttp
from typing_extensions import Literal, TypeVar

from .exceptions import NoContentError, raise_for_code_and_type

RequestVerb = Literal["get", "post", "put", "patch", "delete"]

T = TypeVar("T")

# Module-level shared session. A single ClientSession reuses the underlying TCP
# connection pool across all requests, which avoids the overhead of creating and
# tearing down a new connection on every API call. The session is created lazily
# on first use and intentionally never closed so it can be reused for the
# lifetime of the process. This matches the pattern recommended by aiohttp:
# https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
_shared_session: Optional[aiohttp.ClientSession] = None


def _get_shared_session() -> aiohttp.ClientSession:
    """Return the module-level shared aiohttp session, creating it if needed.

    Using a single session across all AsyncRequest instances allows aiohttp to
    pool and reuse TCP connections, dramatically reducing per-request overhead
    compared to creating a new ClientSession on every call.
    """
    global _shared_session
    if _shared_session is None or _shared_session.closed:
        _shared_session = aiohttp.ClientSession()
    return _shared_session


class AsyncRequestConfig(TypedDict):
    base_url: str
    api_key: str
    headers: Union[Dict[str, str], None]


class AsyncRequest(Generic[T]):
    def __init__(
        self,
        config: AsyncRequestConfig,
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
        # Copy the headers dict so mutations inside this instance never affect
        # the original config dict passed in by the caller.
        raw_headers = config.get("headers", None) or {"Content-Type": "application/json"}
        self.headers: Dict[str, str] = dict(raw_headers)
        self.stream = stream
        self.files = files

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
        session = _get_shared_session()
        resp = await self.make_request(session, url=f"{self.base_url}{self.path}")

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
        session = _get_shared_session()
        resp = await self.make_request(session, url=f"{self.base_url}{self.path}")

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

        Builds a fresh header dict on every call so that:
        - The caller's original headers dict is never mutated.
        - Multipart requests (file uploads) never accidentally carry a
          Content-Type header that would break the multipart boundary.

        Returns:
            Dict[str, str]: Configured HTTP Headers
        """
        h: Dict[str, str] = {
            "Accept": "application/json",
            "x-api-key": f"{self.api_key}",
        }

        # Only set Content-Type for plain JSON requests. Multipart and raw-data
        # requests either let aiohttp set the boundary automatically or rely on
        # the Content-Type that was set explicitly on the config.
        if not self.files and not self.data:
            h["Content-Type"] = "application/json"

        # Merge caller-supplied headers. Work on a copy of self.headers so we
        # never permanently remove keys from the shared config dict.
        caller_headers = dict(self.headers)

        # Strip Content-Type from the caller overrides for multipart requests
        # so that aiohttp can insert the correct multipart/form-data boundary.
        if self.files:
            caller_headers.pop("Content-Type", None)

        h.update(caller_headers)
        return h

    async def perform_streaming(self) -> AsyncGenerator[Union[T, str], None]:
        """
        Async method to stream response from JigsawStack API.

        Returns:
            AsyncGenerator[Union[T, str], None]: A generator of response chunks
        """
        session = _get_shared_session()
        resp = await self.make_request(session, url=f"{self.base_url}{self.path}")

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
            _params = self.__convert_params(params)
        elif files:
            _form_data = aiohttp.FormData()
            _form_data.add_field("file", BytesIO(files["file"]), filename="upload")
            if params and isinstance(params, dict):
                _form_data.add_field("body", json.dumps(params), content_type="application/json")

            headers.pop("Content-Type", None)
        elif data:  # raw data request
            _data = data
        else:  # pure JSON request
            _json = params

        return await session.request(
            verb,
            url,
            params=_params,
            json=_json,
            data=_form_data or _data,
            headers=headers,
        )

    # NOTE: __get_session has been removed in favour of the module-level
    # _get_shared_session() helper. Keeping a session per-request was an
    # aiohttp antipattern that bypassed connection pooling and created
    # unnecessary overhead. All perform_* methods now call _get_shared_session().

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
