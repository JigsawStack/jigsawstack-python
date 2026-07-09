"""
tests/test_headers_mutation.py

Regression tests for the __get_headers mutation bug.

Both Request and AsyncRequest were holding a direct reference to the headers
dict inside the caller's config TypedDict and calling .pop("Content-Type") on
it during multipart file-upload requests.  That permanently modified the shared
config, so every subsequent request reusing the same config would go out without
Content-Type.

These tests are self-contained and require no API key or network access.
"""

from typing import Optional

from jigsawstack.async_request import AsyncRequest, AsyncRequestConfig
from jigsawstack.request import Request, RequestConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sync_config(extra_headers: Optional[dict] = None) -> RequestConfig:
    headers = {"Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    return RequestConfig(base_url="http://test", api_key="key", headers=headers)


def _async_config(extra_headers: Optional[dict] = None) -> AsyncRequestConfig:
    headers = {"Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    return AsyncRequestConfig(base_url="http://test", api_key="key", headers=headers)


# ---------------------------------------------------------------------------
# Sync Request
# ---------------------------------------------------------------------------

class TestSyncRequestHeadersMutation:
    def test_multipart_does_not_mutate_config_headers(self):
        """A multipart request must not remove Content-Type from the config dict."""
        config = _sync_config()
        r = Request(config=config, path="/test", params={}, verb="post", files={"file": b"data"})
        r._Request__get_headers()
        assert "Content-Type" in config["headers"], (
            "__get_headers() stripped Content-Type from the caller's config dict"
        )

    def test_repeated_multipart_calls_do_not_degrade(self):
        """Calling __get_headers() multiple times must always produce the same result."""
        config = _sync_config()
        r = Request(config=config, path="/test", params={}, verb="post", files={"file": b"data"})
        first = r._Request__get_headers()
        second = r._Request__get_headers()
        assert first == second, "__get_headers() returned different results on second call"

    def test_multipart_output_omits_content_type(self):
        """Outgoing headers for a multipart request must not contain Content-Type
        so that the requests library can insert the correct multipart boundary."""
        config = _sync_config()
        r = Request(config=config, path="/test", params={}, verb="post", files={"file": b"data"})
        out = r._Request__get_headers()
        assert "Content-Type" not in out, (
            "Content-Type should be absent from multipart outgoing headers"
        )

    def test_json_request_includes_content_type(self):
        """Plain JSON requests must still set Content-Type: application/json."""
        config = _sync_config()
        r = Request(config=config, path="/test", params={"k": "v"}, verb="post")
        out = r._Request__get_headers()
        assert out.get("Content-Type") == "application/json"

    def test_custom_headers_propagated(self):
        """Any extra caller-supplied headers must survive into the outgoing dict."""
        config = _sync_config(extra_headers={"x-custom": "value"})
        r = Request(config=config, path="/test", params={}, verb="post")
        out = r._Request__get_headers()
        assert out.get("x-custom") == "value"

    def test_second_request_on_same_config_unaffected(self):
        """A second Request built from the same config after a multipart call
        must still produce correct headers — the config was not poisoned."""
        config = _sync_config()
        # First request: multipart — used to trigger the bug
        r1 = Request(config=config, path="/test", params={}, verb="post", files={"file": b"x"})
        r1._Request__get_headers()
        # Second request: plain JSON — previously would be missing Content-Type
        r2 = Request(config=config, path="/test", params={"k": "v"}, verb="post")
        out = r2._Request__get_headers()
        assert out.get("Content-Type") == "application/json", (
            "Config was mutated by the first multipart request; second request lost Content-Type"
        )


# ---------------------------------------------------------------------------
# Async Request
# ---------------------------------------------------------------------------

class TestAsyncRequestHeadersMutation:
    def test_multipart_does_not_mutate_config_headers(self):
        """A multipart request must not remove Content-Type from the config dict."""
        config = _async_config()
        r = AsyncRequest(config=config, path="/test", params={}, verb="post", files={"file": b"data"})
        r._AsyncRequest__get_headers()
        assert "Content-Type" in config["headers"], (
            "__get_headers() stripped Content-Type from the caller's async config dict"
        )

    def test_repeated_multipart_calls_do_not_degrade(self):
        """Calling __get_headers() multiple times must always produce the same result."""
        config = _async_config()
        r = AsyncRequest(config=config, path="/test", params={}, verb="post", files={"file": b"data"})
        first = r._AsyncRequest__get_headers()
        second = r._AsyncRequest__get_headers()
        assert first == second, "__get_headers() returned different results on second call"

    def test_multipart_output_omits_content_type(self):
        """Outgoing headers for a multipart request must not contain Content-Type."""
        config = _async_config()
        r = AsyncRequest(config=config, path="/test", params={}, verb="post", files={"file": b"data"})
        out = r._AsyncRequest__get_headers()
        assert "Content-Type" not in out

    def test_json_request_includes_content_type(self):
        """Plain JSON requests must still set Content-Type: application/json."""
        config = _async_config()
        r = AsyncRequest(config=config, path="/test", params={"k": "v"}, verb="post")
        out = r._AsyncRequest__get_headers()
        assert out.get("Content-Type") == "application/json"

    def test_custom_headers_propagated(self):
        """Any extra caller-supplied headers must survive into the outgoing dict."""
        config = _async_config(extra_headers={"x-custom": "value"})
        r = AsyncRequest(config=config, path="/test", params={}, verb="post")
        out = r._AsyncRequest__get_headers()
        assert out.get("x-custom") == "value"

    def test_second_request_on_same_config_unaffected(self):
        """A second AsyncRequest built from the same config after a multipart call
        must still produce correct headers."""
        config = _async_config()
        r1 = AsyncRequest(config=config, path="/test", params={}, verb="post", files={"file": b"x"})
        r1._AsyncRequest__get_headers()
        r2 = AsyncRequest(config=config, path="/test", params={"k": "v"}, verb="post")
        out = r2._AsyncRequest__get_headers()
        assert out.get("Content-Type") == "application/json", (
            "Config was mutated by the first multipart request; second request lost Content-Type"
        )
