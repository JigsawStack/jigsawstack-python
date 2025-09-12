import logging
import os

import pytest
from dotenv import load_dotenv

import jigsawstack
from jigsawstack.exceptions import JigsawStackError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))

TEST_CASES = [
    {
        "name": "text_classification_programming",
        "params": {
            "dataset": [
                {"type": "text", "value": "I love programming"},
                {"type": "text", "value": "I love reading books"},
                {"type": "text", "value": "I love watching movies"},
                {"type": "text", "value": "I love playing games"},
            ],
            "labels": [
                {"type": "text", "value": "programming"},
                {"type": "text", "value": "reading"},
                {"type": "text", "value": "watching"},
                {"type": "text", "value": "playing"},
            ],
        },
    },
    {
        "name": "text_classification_sentiment",
        "params": {
            "dataset": [
                {"type": "text", "value": "This is awesome!"},
                {"type": "text", "value": "I hate this product"},
                {"type": "text", "value": "It's okay, nothing special"},
            ],
            "labels": [
                {"type": "text", "value": "positive"},
                {"type": "text", "value": "negative"},
                {"type": "text", "value": "neutral"},
            ],
        },
    },
    {
        "name": "text_classification_weather",
        "params": {
            "dataset": [
                {"type": "text", "value": "The weather is sunny today"},
                {"type": "text", "value": "It's raining heavily outside"},
                {"type": "text", "value": "Snow is falling gently"},
            ],
            "labels": [
                {"type": "text", "value": "sunny"},
                {"type": "text", "value": "rainy"},
                {"type": "text", "value": "snowy"},
            ],
        },
    },
    {
        "name": "image_classification_fruits",
        "params": {
            "dataset": [
                {
                    "type": "image",
                    "value": "https://as2.ftcdn.net/v2/jpg/02/24/11/57/1000_F_224115780_2ssvcCoTfQrx68Qsl5NxtVIDFWKtAgq2.jpg",
                },
                {
                    "type": "image",
                    "value": "https://t3.ftcdn.net/jpg/02/95/44/22/240_F_295442295_OXsXOmLmqBUfZreTnGo9PREuAPSLQhff.jpg",
                },
                {
                    "type": "image",
                    "value": "https://as1.ftcdn.net/v2/jpg/05/54/94/46/1000_F_554944613_okdr3fBwcE9kTOgbLp4BrtVi8zcKFWdP.jpg",
                },
            ],
            "labels": [
                {"type": "text", "value": "banana"},
                {
                    "type": "image",
                    "value": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg",
                },
                {"type": "text", "value": "kisses"},
            ],
        },
    },
    {
        "name": "text_classification_multiple_labels",
        "params": {
            "dataset": [
                {
                    "type": "text",
                    "value": "Python is a great programming language for data science",
                },
                {
                    "type": "text",
                    "value": "JavaScript is essential for web development",
                },
            ],
            "labels": [
                {"type": "text", "value": "programming"},
                {"type": "text", "value": "data science"},
                {"type": "text", "value": "web development"},
            ],
            "multiple_labels": True,
        },
    },
    {
        "name": "image_classification_with_multiple_labels",
        "params": {
            "dataset": [
                {
                    "type": "image",
                    "value": "https://as2.ftcdn.net/v2/jpg/02/24/11/57/1000_F_224115780_2ssvcCoTfQrx68Qsl5NxtVIDFWKtAgq2.jpg",
                },
                {
                    "type": "image",
                    "value": "https://t3.ftcdn.net/jpg/02/95/44/22/240_F_295442295_OXsXOmLmqBUfZreTnGo9PREuAPSLQhff.jpg",
                },
                {
                    "type": "image",
                    "value": "https://as1.ftcdn.net/v2/jpg/05/54/94/46/1000_F_554944613_okdr3fBwcE9kTOgbLp4BrtVi8zcKFWdP.jpg",
                },
            ],
            "labels": [
                {"type": "text", "value": "banana"},
                {
                    "type": "image",
                    "value": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg",
                },
                {"type": "text", "value": "kisses"},
            ],
        },
    },
]


class TestClassificationSync:
    """Test synchronous classification methods"""

    sync_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_classification(self, test_case):
        """Test synchronous classification with various inputs"""
        try:
            result = jigsaw.classification(test_case["params"])
            assert result["success"]
            assert "predictions" in result
            if test_case.get("multiple_labels"):
                # Ensure predictions are lists when multiple_labels is True
                for prediction in result["predictions"]:
                    assert isinstance(prediction, list)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestClassificationAsync:
    """Test asynchronous classification methods"""

    async_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_classification_async(self, test_case):
        """Test asynchronous classification with various inputs"""
        try:
            result = await async_jigsaw.classification(test_case["params"])
            assert result["success"]
            assert "predictions" in result

            if test_case.get("multiple_labels"):
                # Ensure predictions are lists when multiple_labels is True
                for prediction in result["predictions"]:
                    assert isinstance(prediction, list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
