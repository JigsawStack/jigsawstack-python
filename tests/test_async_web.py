from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import AsyncJigsawStack
import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_async_web_search_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.web.search({"query": "JigsawStack fund raising"})
            # logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


def test_async_web_search_suggestion_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.web.search_suggestion({"query": "Lagos"})
            logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())
