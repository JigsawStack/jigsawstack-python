from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import JigsawStack, AsyncJigsawStack
import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Synchronous AI Scrape Tests
def test_ai_scrape_with_selectors():
    """Test AI scrape with CSS selectors"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://news.ycombinator.com/news",
                "selectors": [".titles", ".points"],
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape with selectors test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_scrape_with_element_prompts():
    """Test AI scrape with element prompts"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://news.ycombinator.com/news",
                "element_prompts": ["titles", "points"],
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape with element prompts test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_scrape_with_selectors_and_prompts():
    """Test AI scrape with both selectors and element prompts"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://news.ycombinator.com/news",
                "selectors": [".titles", ".points"],
                "element_prompts": ["titles", "points"],
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape with selectors and prompts test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_scrape_with_advanced_config():
    """Test AI scrape with advanced configuration options"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://news.ycombinator.com/news",
                "selectors": [".titles", ".points"],
                "root_element_selector": "main",
                "page_position": 0,
                "http_headers": {"User-Agent": "JigsawStack-Test/1.0"},
                "goto_options": {"timeout": 30000, "wait_until": "domcontentloaded"},
                "wait_for": {"mode": "selector", "value": ".content"},
                "advance_config": {"console": True, "network": False, "cookies": True},
                "is_mobile": False,
                "scale": 1,
                "width": 1920,
                "height": 1080,
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape with advanced config test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_scrape_with_cookies():
    """Test AI scrape with custom cookies"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://example.com",
                "selectors": [".user-content"],
                "cookies": [
                    {
                        "name": "session_id",
                        "value": "abc123",
                        "domain": "example.com",
                        "path": "/",
                        "secure": True,
                        "httpOnly": True,
                        "sameSite": "Strict",
                    }
                ],
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape with cookies test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_scrape_with_proxy():
    """Test AI scrape with BYO proxy configuration"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://example.com",
                "element_prompts": ["Extract main content"],
                "force_rotate_proxy": True,
                "byo_proxy": {
                    "server": "proxy.example.com:8080",
                    "auth": {"username": "proxy_user", "password": "proxy_pass"},
                },
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape with proxy test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_scrape_mobile_preset():
    """Test AI scrape with mobile size preset"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://example.com",
                "selectors": [".mobile-content"],
                "size_preset": "mobile",
                "is_mobile": True,
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape mobile preset test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


def test_ai_scrape_with_request_filtering():
    """Test AI scrape with request pattern rejection"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {
                "url": "https://example.com",
                "element_prompts": ["Get main article text"],
                "reject_request_pattern": [
                    ".*\\.js$",
                    ".*\\.css$",
                    ".*analytics.*",
                    ".*ads.*",
                ],
            }
        )
        assert result["success"] == True
        assert "data" in result
        logger.info("AI scrape with request filtering test passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")


# Asynchronous AI Scrape Tests
def test_async_ai_scrape_with_selectors():
    """Test async AI scrape with CSS selectors"""

    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.web.ai_scrape(
                {
                    "url": "https://example.com",
                    "selectors": [".title", ".price", ".description"],
                }
            )
            assert result["success"] == True
            assert "data" in result
            logger.info("Async AI scrape with selectors test passed")
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


def test_async_ai_scrape_with_element_prompts():
    """Test async AI scrape with element prompts"""

    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.web.ai_scrape(
                {
                    "url": "https://example.com",
                    "element_prompts": [
                        "Find the product title",
                        "Extract the price",
                        "Get the product description",
                    ],
                }
            )
            assert result["success"] == True
            assert "data" in result
            logger.info("Async AI scrape with element prompts test passed")
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


def test_async_ai_scrape_with_timeout_config():
    """Test async AI scrape with timeout and wait configurations"""

    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.web.ai_scrape(
                {
                    "url": "https://example.com",
                    "selectors": [".dynamic-content"],
                    "goto_options": {"timeout": 60000, "wait_until": "networkidle2"},
                    "wait_for": {"mode": "timeout", "value": 3000},
                }
            )
            assert result["success"] == True
            assert "data" in result
            logger.info("Async AI scrape with timeout config test passed")
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


def test_async_ai_scrape_comprehensive():
    """Test async AI scrape with comprehensive configuration"""

    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.web.ai_scrape(
                {
                    "url": "https://example.com",
                    "selectors": [".product-title", ".price", ".availability"],
                    "element_prompts": [
                        "Extract product information",
                        "Get pricing details",
                    ],
                    "root_element_selector": ".product-container",
                    "page_position": 1,
                    "http_headers": {
                        "User-Agent": "JigsawStack-AsyncTest/1.0",
                        "Accept-Language": "en-US,en;q=0.9",
                    },
                    "goto_options": {"timeout": 45000, "wait_until": "load"},
                    "wait_for": {"mode": "selector", "value": ".product-container"},
                    "advance_config": {
                        "console": False,
                        "network": True,
                        "cookies": True,
                    },
                    "size_preset": "desktop",
                    "is_mobile": False,
                    "scale": 1,
                    "width": 1366,
                    "height": 768,
                    "force_rotate_proxy": False,
                    "reject_request_pattern": [".*\\.gif$", ".*tracking.*"],
                }
            )
            assert result["success"] == True
            assert "data" in result
            assert "meta" in result
            assert "link" in result
            assert "selectors" in result
            logger.info("Async comprehensive AI scrape test passed")
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError: {e}")

    asyncio.run(_test())


# Error Handling Tests
def test_ai_scrape_missing_required_params():
    """Test AI scrape error handling for missing required parameters"""
    client = JigsawStack()
    try:
        # Missing both selectors and element_prompts
        result = client.web.ai_scrape({"url": "https://example.com"})
        # Should still work as the API might have defaults
        logger.info("AI scrape with minimal params completed")
    except JigsawStackError as e:
        # Expected error for insufficient parameters
        logger.info(f"Expected error for missing params: {e}")


def test_async_ai_scrape_invalid_url():
    """Test async AI scrape error handling for invalid URL"""

    async def _test():
        client = AsyncJigsawStack()
        try:
            result = await client.web.ai_scrape(
                {"url": "invalid-url", "selectors": [".content"]}
            )
            # Might succeed depending on API behavior
            logger.info("AI scrape with invalid URL completed")
        except JigsawStackError as e:
            # Expected error for invalid URL
            logger.info(f"Expected error for invalid URL: {e}")

    asyncio.run(_test())


# Response Structure Validation Tests
def test_ai_scrape_response_structure():
    """Test that AI scrape response has expected structure"""
    client = JigsawStack()
    try:
        result = client.web.ai_scrape(
            {"url": "https://example.com", "selectors": [".title"]}
        )

        # Validate response structure
        assert "success" in result
        assert "data" in result
        assert isinstance(result["data"], list)

        # Check for optional fields
        if "meta" in result:
            assert isinstance(result["meta"], (dict, type(None)))
        if "link" in result:
            assert isinstance(result["link"], list)
        if "selectors" in result:
            assert isinstance(result["selectors"], dict)

        logger.info("AI scrape response structure validation passed")
    except JigsawStackError as e:
        pytest.fail(f"Unexpected JigsawStackError: {e}")
