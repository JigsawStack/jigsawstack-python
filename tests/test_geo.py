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
def test_async_country_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.geo.country({"country_code": "SGP"})
            logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
def test_async_search_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.geo.search({"search_value": "Nigeria"})
            logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())
