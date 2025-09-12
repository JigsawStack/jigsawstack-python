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
        "name": "positive_sentiment_excited",
        "params": {
            "text": "I am so excited about this new product! It's absolutely amazing and I can't wait to use it every day."
        },
    },
    {
        "name": "negative_sentiment_disappointed",
        "params": {
            "text": "I'm really disappointed with this purchase. The quality is terrible and it broke after just one day."
        },
    },
    {
        "name": "neutral_sentiment_factual",
        "params": {
            "text": "The meeting is scheduled for 3 PM tomorrow in conference room B."
        },
    },
    {
        "name": "mixed_sentiment_paragraph",
        "params": {
            "text": "The product arrived on time which was great. However, the packaging was damaged. The item itself works fine, but the instructions were confusing."
        },
    },
    {
        "name": "positive_sentiment_love",
        "params": {
            "text": "I absolutely love this! Best purchase I've made all year. Highly recommend to everyone!"
        },
    },
    {
        "name": "negative_sentiment_angry",
        "params": {
            "text": "This is unacceptable! I want a refund immediately. Worst customer service ever!"
        },
    },
    {
        "name": "single_sentence_positive",
        "params": {"text": "This made my day!"},
    },
    {
        "name": "single_sentence_negative",
        "params": {"text": "I hate this."},
    },
    {
        "name": "complex_multi_sentence",
        "params": {
            "text": "The first part of the movie was boring and I almost fell asleep. But then it got really exciting! The ending was spectacular and now it's one of my favorites."
        },
    },
    {
        "name": "question_sentiment",
        "params": {
            "text": "Why is this product so amazing? I can't believe how well it works!"
        },
    },
]


class TestSentimentSync:
    """Test synchronous sentiment analysis methods"""

    sync_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_sentiment_analysis(self, test_case):
        """Test synchronous sentiment analysis with various inputs"""
        try:
            result = jigsaw.sentiment(test_case["params"])

            assert result["success"]
            assert "sentiment" in result
            assert "emotion" in result["sentiment"]
            assert "sentiment" in result["sentiment"]
            assert "score" in result["sentiment"]

            # Check if sentences analysis is included
            if "sentences" in result["sentiment"]:
                assert isinstance(result["sentiment"]["sentences"], list)
                for sentence in result["sentiment"]["sentences"]:
                    assert "text" in sentence
                    assert "sentiment" in sentence
                    assert "emotion" in sentence
                    assert "score" in sentence

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSentimentAsync:
    """Test asynchronous sentiment analysis methods"""

    async_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_sentiment_analysis_async(self, test_case):
        """Test asynchronous sentiment analysis with various inputs"""
        try:
            result = await async_jigsaw.sentiment(test_case["params"])

            assert result["success"]
            assert "sentiment" in result
            assert "emotion" in result["sentiment"]
            assert "sentiment" in result["sentiment"]
            assert "score" in result["sentiment"]

            # Check if sentences analysis is included
            if "sentences" in result["sentiment"]:
                assert isinstance(result["sentiment"]["sentences"], list)
                for sentence in result["sentiment"]["sentences"]:
                    assert "text" in sentence
                    assert "sentiment" in sentence
                    assert "emotion" in sentence
                    assert "score" in sentence

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
