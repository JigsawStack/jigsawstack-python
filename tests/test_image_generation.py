from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest
import asyncio
import logging
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack()
async_jigsaw = jigsawstack.AsyncJigsawStack()


def test_image_generation_response():
    async def _test():
        client = jigsawstack.AsyncJigsawStack()
        try:
            result = await client.image_generation({
                "prompt": "A beautiful mountain landscape at sunset",
                "aspect_ratio": "16:9"
            })
            # Just check if we got some data back
            assert result is not None
            assert len(result) > 0
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


def test_image_generation_with_advanced_config():
    async def _test():
        client = jigsawstack.AsyncJigsawStack()
        try:
            result = await client.image_generation({
                "prompt": "A beautiful mountain landscape at sunset",
                "output_format": "png",
                "advance_config": {
                    "negative_prompt": "blurry, low quality",
                    "guidance": 7,
                    "seed": 42
                }
            })
            # Just check if we got some data back
            assert result is not None
            assert len(result) > 0
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())