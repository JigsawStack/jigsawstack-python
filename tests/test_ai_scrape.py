import logging
import os

import pytest
from dotenv import load_dotenv

import jigsawstack
from jigsawstack.exceptions import JigsawStackError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))

URL = "https://jigsawstack.com"

# AI Scrape Test Cases
AI_SCRAPE_TEST_CASES = [
    {
        "name": "scrape_with_element_prompts",
        "params": {
            "url": URL,
            "element_prompts": ["title", "main content", "navigation links"],
        },
    },
    {
        "name": "scrape_with_selectors",
        "params": {
            "url": URL,
            "selectors": ["h1", "p", "a"],
        },
    },
    {
        "name": "scrape_with_features",
        "params": {
            "url": URL,
            "element_prompts": ["title"],
            "features": ["meta", "link"],
        },
    },
    {
        "name": "scrape_with_root_element",
        "params": {
            "url": URL,
            "element_prompts": ["content"],
            "root_element_selector": "main",
        },
    },
    {
        "name": "scrape_with_wait_for_timeout",
        "params": {
            "url": URL,
            "element_prompts": ["content"],
            "wait_for": {"mode": "timeout", "value": 3000},
        },
    },
    {
        "name": "scrape_mobile_view",
        "params": {
            "url": URL,
            "element_prompts": ["mobile menu"],
            "is_mobile": True,
        },
    },
    {
        "name": "scrape_with_cookies",
        "params": {
            "url": URL,
            "element_prompts": ["user data"],
            "cookies": [{"name": "session", "value": "test123", "domain": "example.com"}],
        },
    },
    {
        "name": "scrape_with_advance_config",
        "params": {
            "url": URL,
            "element_prompts": ["content"],
            "advance_config": {"console": True, "network": True, "cookies": True},
        },
    },
]


class TestAIScrapeSync:
    """Test synchronous AI scrape methods"""

    @pytest.mark.parametrize(
        "test_case",
        AI_SCRAPE_TEST_CASES,
        ids=[tc["name"] for tc in AI_SCRAPE_TEST_CASES],
    )
    def test_ai_scrape(self, test_case):
        """Test synchronous AI scrape with various inputs"""
        try:
            result = jigsaw.web.ai_scrape(test_case["params"])

            assert result["success"]
            assert "data" in result
            assert isinstance(result["data"], list)

            # Check for optional features
            if "meta" in test_case["params"].get("features", []):
                assert "meta" in result
            if "link" in test_case["params"].get("features", []):
                assert "link" in result
                assert isinstance(result["link"], list)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestAIScrapeAsync:
    """Test asynchronous AI scrape methods"""

    @pytest.mark.parametrize(
        "test_case",
        AI_SCRAPE_TEST_CASES,
        ids=[tc["name"] for tc in AI_SCRAPE_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_ai_scrape_async(self, test_case):
        """Test asynchronous AI scrape with various inputs"""
        try:
            result = await async_jigsaw.web.ai_scrape(test_case["params"])

            assert result["success"]
            assert "data" in result
            assert isinstance(result["data"], list)

            # Check for optional features
            if "meta" in test_case["params"].get("features", []):
                assert "meta" in result
            if "link" in test_case["params"].get("features", []):
                assert "link" in result
                assert isinstance(result["link"], list)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
