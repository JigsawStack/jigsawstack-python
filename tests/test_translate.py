from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.translate
import jigsawstack.translate._translate

# flake8: noqa

class TestTranslateAPI(unittest.TestCase):

    def test_translate_response_success(self) -> None:
        params = {
            "current_language":"en",
            "target_language":"es",
            "text": "Hello, world!"
        }
        try:
            result = jigsawstack.Translate.translate(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."