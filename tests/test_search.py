from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.search
import jigsawstack.search._search
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.translate
import jigsawstack.translate._translate

# flake8: noq

class TestSearchAPI(unittest.TestCase):
    def test_search_suggestion_response_success(self) -> None:
        params = {
            "query": "Time Square New Yor"
        }
        try:
            result = jigsawstack.search._search.suggestion(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_ai_search_response_success(self) -> None:
        params = {
            "query": "Time Square New Yor"
        }
        try:
            result = jigsawstack.search._search.ai(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."