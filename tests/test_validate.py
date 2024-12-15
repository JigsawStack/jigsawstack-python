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
def test_async_spam_check_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.validate.spamcheck({"text": "I am happy!"})
            logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
def test_async_spell_check_response():
    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.validate.spellcheck(
                {
                    "text": "All the world's a stage, and all the men and women merely players. They have their exits and their entrances; And one man in his time plays many parts"
                }
            )
            logger.info(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())
