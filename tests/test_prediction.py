from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.prediction
import jigsawstack.prediction._prediction 
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.translate
import jigsawstack.translate._translate
import pytest
# flake8: noqa


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")

class TestPredictionAPI(unittest.TestCase):

    def test_sentiment_response_success(self) -> None:
        params = {
            "dataset": [  {
    "date": "2023-10-10",
    "value": 10,
  },
  {
    "date": "2023-09-10",
    "value": 5,
  },{
    "date": "2023-08-10",
    "value": 40,
  },
  {
    "date": "2023-07-10",
    "value": 30,
  },
  {
    "date": "2023-06-10",
    "value": 10,
  },
  {
    "date": "2023-05-10",
    "value": 10,
  }
  ]
        }
        try:
            result = jigsawstack.Prediction.predict(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."