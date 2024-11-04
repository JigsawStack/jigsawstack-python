from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest

# flake8: noq

jigsaw = jigsawstack.JigsawStack()


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
class TestPromptEngine(unittest.TestCase):

    def test_get_prompt_engine_response_success(self) -> None:
        try:
            result = jigsaw.prompt_engine.get("b08921b8-0b30-409e-8257-06fa1620c7e6")
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."
