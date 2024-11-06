from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest

# flake8: noq

jigsaw = jigsawstack.JigsawStack()


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
class TestSearchAPI(unittest.TestCase):

    def test_search_suggestion_response_success(self) -> None:
        params = {"query": "Time Square New Yor"}
        try:
            result = jigsaw.search.suggestion(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_ai_search_response_success(self) -> None:
        params = {"query": "Time Square New Yor"}
        try:
            result = jigsaw.search.ai_search(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."
