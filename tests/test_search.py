from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack()
async_jigsaw = jigsawstack.AsyncJigsawStack()


def test_search_suggestion_response():
    try:
        result = jigsaw.web.search({"query": "Where is San Francisco"})
        assert result["success"] == True
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_search_response():
    try:
        result = jigsaw.web.search({"query": "Where is San Francisco"})
        assert result["success"] == True  
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_search_suggestion_response_async():
    async def _test():
        client = jigsawstack.AsyncJigsawStack()
        try:
            result = await client.web.search({"query": "Where is San Francisco"})
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


def test_ai_search_response_async():
    async def _test():
        client = jigsawstack.AsyncJigsawStack()
        try:
            result = await client.web.search({"query": "Where is San Francisco"})
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())