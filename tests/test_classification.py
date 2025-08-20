from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import JigsawStack, AsyncJigsawStack
import asyncio
import logging

import pytest 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = JigsawStack()
async_client = AsyncJigsawStack()


class TestClassificationAPI(unittest.TestCase):
    def test_classification_text_success_response(self):
        params = {
            "dataset": [
                {"type": "text", "value": "Hello"},
                {"type": "text", "value": "World"}
            ],
            "labels": [
                {"type": "text", "value": "Greeting"},
                {"type": "text", "value": "Object"}
            ]
        }
        try:
            result = client.classification.text(params)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    def test_classification_text_async_success_response(self):
        async def _test():
            params = {
                "dataset": [
                    {"type": "text", "value": "Hello"},
                    {"type": "text", "value": "World"}
                ],
                "labels": [
                    {"type": "text", "value": "Greeting"},
                    {"type": "text", "value": "Object"}
                ]
            }
            try:
                result = await async_client.classification.text(params)
                assert result["success"] == True
            except JigsawStackError as e:
                pytest.fail(f"Unexpected JigsawStackError: {e}")

        asyncio.run(_test())

    def test_classification_text_with_multiple_labels(self):
        params = {
            "dataset": [
                {"type": "text", "value": "This is a positive and happy message"}
            ],
            "labels": [
                {"type": "text", "value": "positive"},
                {"type": "text", "value": "negative"},
                {"type": "text", "value": "happy"},
                {"type": "text", "value": "sad"}
            ],
            "multiple_labels": True
        }
        try:
            result = client.classification.text(params)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    def test_classification_image_success_response(self):
        params = {
            "dataset": [
                {"type": "image", "value": "https://example.com/image1.jpg"},
                {"type": "image", "value": "https://example.com/image2.jpg"}
            ],
            "labels": [
                {"type": "text", "value": "Cat"},
                {"type": "text", "value": "Dog"}
            ]
        }
        try:
            result = client.classification.image(params)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    def test_classification_image_async_success_response(self):
        async def _test():
            params = {
                "dataset": [
                    {"type": "image", "value": "https://example.com/image1.jpg"},
                    {"type": "image", "value": "https://example.com/image2.jpg"}
                ],
                "labels": [
                    {"type": "text", "value": "Cat"},
                    {"type": "text", "value": "Dog"}
                ]
            }
            try:
                result = await async_client.classification.image(params)
                assert result["success"] == True
            except JigsawStackError as e:
                pytest.fail(f"Unexpected JigsawStackError: {e}")

        asyncio.run(_test())

    def test_classification_image_with_multiple_labels(self):
        params = {
            "dataset": [
                {"type": "image", "value": "https://example.com/pet_image.jpg"}
            ],
            "labels": [
                {"type": "text", "value": "cute"},
                {"type": "text", "value": "fluffy"},
                {"type": "text", "value": "animal"},
                {"type": "text", "value": "pet"}
            ],
            "multiple_labels": True
        }
        try:
            result = client.classification.image(params)
            assert result["success"] == True
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

