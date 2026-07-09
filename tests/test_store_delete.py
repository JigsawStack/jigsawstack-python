"""
tests/test_store_delete.py

Tests for claim 3: Store.delete and AsyncStore.delete passed params=key
(a raw string) instead of params={}.

For a DELETE /store/file/read/{key} request the key is already in the URL
path; passing a raw string as params would append it as a malformed query
string.  The fix is params={}.
No real network calls are made.
"""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from jigsawstack.store import AsyncStore, Store
from jigsawstack.request import RequestConfig
from jigsawstack.async_request import AsyncRequestConfig


def _sync_store() -> Store:
    return Store(api_key="key", base_url="http://test")


def _async_store() -> AsyncStore:
    return AsyncStore(api_key="key", base_url="http://test")


class TestStoreDeleteParams:
    def test_sync_delete_passes_empty_params(self):
        """Request built by Store.delete must use params={}, not params=key."""
        captured = {}

        original_init = __import__("jigsawstack.request", fromlist=["Request"]).Request.__init__

        def capturing_init(self, config, path, params, verb, **kwargs):
            captured["params"] = params
            captured["verb"] = verb
            # minimal setup so perform_with_content() doesn't blow up
            self.path = path
            self.params = params
            self.verb = verb
            self.base_url = config.get("base_url")
            self.api_key = config.get("api_key")
            self.data = None
            self.headers = {"Content-Type": "application/json"}
            self.stream = False
            self.files = None

        with patch("jigsawstack.store.Request.__init__", capturing_init), \
             patch("jigsawstack.store.Request.perform_with_content", return_value={"success": True}):
            _sync_store().delete("my-key")

        assert captured["verb"] == "delete"
        assert captured["params"] == {}, (
            f"Expected params={{}}, got {captured['params']!r}. "
            "Passing the key string as params appends a malformed query string."
        )

    def test_async_delete_passes_empty_params(self):
        """AsyncRequest built by AsyncStore.delete must use params={}, not params=key."""
        from unittest.mock import AsyncMock
        from jigsawstack.async_request import AsyncRequest as AR

        calls = []
        original_init = AR.__init__

        def spy_init(self, config, path, params, verb, **kw):
            calls.append({"params": params, "verb": verb})
            original_init(self, config=config, path=path, params=params, verb=verb, **kw)

        async def run():
            with patch.object(AR, "__init__", spy_init), \
                 patch.object(AR, "perform_with_content", new_callable=AsyncMock,
                              return_value={"success": True}):
                store = _async_store()
                await store.delete("my-key")

        asyncio.run(run())

        assert len(calls) == 1
        assert calls[0]["verb"] == "delete"
        assert calls[0]["params"] == {}, (
            f"Expected params={{}}, got {calls[0]['params']!r}."
        )

    def test_sync_delete_key_in_url_path(self):
        """The key must appear in the request path, not as a parameter."""
        captured_path = {}

        def capturing_init(self, config, path, params, verb, **kwargs):
            captured_path["path"] = path
            self.path = path
            self.params = params
            self.verb = verb
            self.base_url = config.get("base_url")
            self.api_key = config.get("api_key")
            self.data = None
            self.headers = {"Content-Type": "application/json"}
            self.stream = False
            self.files = None

        with patch("jigsawstack.store.Request.__init__", capturing_init), \
             patch("jigsawstack.store.Request.perform_with_content", return_value={"success": True}):
            _sync_store().delete("my-key")

        assert "my-key" in captured_path["path"]
