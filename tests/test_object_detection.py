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


def test_object_detection_response():
    try:
        result = jigsaw.vision.object_detection({"url": "https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Collabo%201080x842.jpg"})
        print(result)
        assert result["success"] == True
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_object_detection_response_async():
    async def _test():
        client = jigsawstack.AsyncJigsawStack()
        try:
            result = await client.vision.object_detection({"url": "https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Collabo%201080x842.jpg"})
            print(result)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())

