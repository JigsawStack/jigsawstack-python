from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import AsyncJigsawStack
import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
def test_async_kv_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.store.kv.add(
                {"key": "hello", "value": "world", "encrypt": False}
            )
            logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


def test_async_retriev_kv_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.store.kv.get("hello")
            logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())
