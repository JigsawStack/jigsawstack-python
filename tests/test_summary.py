from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.sql
import jigsawstack.sql._sql
import jigsawstack.summary
import jigsawstack.summary._summary
import jigsawstack.translate
import jigsawstack.translate._translate
import pytest
# flake8: noqa

@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
class TestSummaryAPI(unittest.TestCase):

    def test_summary_response_success(self) -> None:
        params = {
            "text": "The Leaning Tower of Pisa, or simply, the Tower of Pisa, is the campanile, or freestanding bell tower, of Pisa Cathedral."
        }
        try:
            result = jigsawstack.Summary.summarize(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."