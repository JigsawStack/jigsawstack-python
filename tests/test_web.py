from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.translate
import jigsawstack.translate._translate
import jigsawstack.web
import jigsawstack

# flake8: noqa
class TestWebAPI(unittest.TestCase):

    def test_ai_scrape_success_response(self) -> None:
        params = {
         "url": "https://supabase.com/pricing",
         "element_prompts": ["Plan title", "Plan price"],
        }
        try:
            result = jigsawstack.Web.ai_scrape(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_scrape_success_response(self) -> None:
        params = {
         "url": "https://supabase.com/pricing",
        }
        try:
            result = jigsawstack.Web.scrape(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_dns_success_response(self) -> None:

        params = {
                "url": "https://supabase.com/pricing",
        }
        try:
            result = jigsawstack.Web.dns(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."