from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.translate
import jigsawstack.translate._translate

# flake8: noqa


class TestSentimentAPI(unittest.TestCase):

    def test_sentiment_response_success(self) -> None:
        params = {
            "text": "I am so excited"
        }
        try:
            result = jigsawstack.sentiment._sentiment.sentiment(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."