from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.translate
import jigsawstack.translate._translate
import pytest
# flake8: noqa

@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
class TestSentimentAPI(unittest.TestCase):

    def test_sentiment_response_success(self) -> None:
        params = {
            "text": "I am so excited"
        }
        try:
            result = jigsawstack.Sentiment.analyze(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."