from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import JigsawStack

import pytest

# flake8: noqa

client = JigsawStack()


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
class TestWebAPI(unittest.TestCase):
    def test_ai_scrape_success_response(self) -> None:
        params = {
            "url": "https://supabase.com/pricing",
            "element_prompts": ["Plan title", "Plan price"],
        }
        try:
            result = client.file.upload(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_scrape_success_response(self) -> None:
        params = {
            "url": "https://supabase.com/pricing",
        }
        try:
            result = client.web.scrape(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_dns_success_response(self) -> None:

        params = {
            "url": "https://supabase.com/pricing",
        }
        try:
            result = client.web.dns(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."
