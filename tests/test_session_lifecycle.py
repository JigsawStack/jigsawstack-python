"""
tests/test_session_lifecycle.py

Tests for claim 1: AsyncJigsawStack session management.

Verifies that:
- Without __aenter__, each request creates its own temporary session.
- With __aenter__, a single shared ClientSession is injected into every
  service config and reused across requests.
- __aexit__ / aclose() removes the session from all configs and closes it.
- Re-entering after aclose() works correctly (fresh session).
No real network calls are made.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from jigsawstack import AsyncJigsawStack
from jigsawstack.async_request import AsyncRequest, AsyncRequestConfig


# ---------------------------------------------------------------------------
# Unit: _SessionContext
# ---------------------------------------------------------------------------

class TestSessionContext:
    def test_reuses_session_without_closing(self):
        from jigsawstack.async_request import _SessionContext

        mock_session = MagicMock(spec=aiohttp.ClientSession)
        ctx = _SessionContext(mock_session)

        async def run():
            async with ctx as s:
                assert s is mock_session
            mock_session.close.assert_not_called()

        asyncio.run(run())


# ---------------------------------------------------------------------------
# Unit: AsyncRequest picks up shared session from config
# ---------------------------------------------------------------------------

class TestAsyncRequestSessionInjection:
    def test_no_session_in_config_uses_own_session(self):
        config = AsyncRequestConfig(base_url="http://test", api_key="key", headers=None)
        r = AsyncRequest(config=config, path="/x", params={}, verb="get")
        assert r._shared_session is None

    def test_session_in_config_is_stored(self):
        mock_session = MagicMock(spec=aiohttp.ClientSession)
        config = AsyncRequestConfig(base_url="http://test", api_key="key", headers=None)
        config["session"] = mock_session
        r = AsyncRequest(config=config, path="/x", params={}, verb="get")
        assert r._shared_session is mock_session


# ---------------------------------------------------------------------------
# Integration: AsyncJigsawStack as async context manager
# ---------------------------------------------------------------------------

class TestAsyncJigsawStackContextManager:
    def test_no_session_before_enter(self):
        client = AsyncJigsawStack(api_key="test-key")
        assert client._session is None
        # configs should not have a session key yet
        for svc in client._async_services:
            assert svc.config.get("session") is None

    def test_enter_injects_session_into_all_services(self):
        async def run():
            async with AsyncJigsawStack(api_key="test-key") as client:
                assert isinstance(client._session, aiohttp.ClientSession)
                for svc in client._async_services:
                    assert svc.config.get("session") is client._session
                await client._session.close()  # prevent ResourceWarning in test

        asyncio.run(run())

    def test_exit_clears_session_from_all_services(self):
        async def run():
            client = AsyncJigsawStack(api_key="test-key")
            await client.__aenter__()
            session = client._session
            await client.__aexit__(None, None, None)

            assert client._session is None
            assert session.closed
            for svc in client._async_services:
                assert svc.config.get("session") is None

        asyncio.run(run())

    def test_aclose_is_idempotent(self):
        async def run():
            async with AsyncJigsawStack(api_key="test-key") as client:
                pass
            await client.aclose()

        asyncio.run(run())

    def test_reenter_after_aclose_creates_fresh_session(self):
        async def run():
            client = AsyncJigsawStack(api_key="test-key")
            await client.__aenter__()
            first_session = client._session
            await client.aclose()

            await client.__aenter__()
            second_session = client._session
            assert second_session is not first_session
            assert isinstance(second_session, aiohttp.ClientSession)
            await client.aclose()

        asyncio.run(run())
