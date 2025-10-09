from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#   const client = JigsawStack({
#     apiKey,
#     baseURL: process.env.JIGSAWSTACK_BASE_URL ? `${process.env.JIGSAWSTACK_BASE_URL}/api` : "https://api.jigsawstack.com",
#     headers: { "x-jigsaw-skip-cache": "true" },
#   });

jigsaw = jigsawstack.JigsawStack(
    api_key=os.getenv("JIGSAWSTACK_API_KEY"),
    base_url=os.getenv("JIGSAWSTACK_BASE_URL") + "/api"
    if os.getenv("JIGSAWSTACK_BASE_URL")
    else "https://api.jigsawstack.com",
    headers={"x-jigsaw-skip-cache": "true"},
)
async_jigsaw = jigsawstack.AsyncJigsawStack(
    api_key=os.getenv("JIGSAWSTACK_API_KEY"),
    base_url=os.getenv("JIGSAWSTACK_BASE_URL") + "/api"
    if os.getenv("JIGSAWSTACK_BASE_URL")
    else "https://api.jigsawstack.com",
    headers={"x-jigsaw-skip-cache": "true"},
)

URL = "https://jigsawstack.com"

# HTML to Any Test Cases
HTML_TO_ANY_TEST_CASES = [
    {
        "name": "html_to_pdf_url",
        "params": {
            "url": URL,
            "type": "pdf",
            "return_type": "url",
        },
    },
    {
        "name": "html_to_png_base64",
        "params": {
            "url": URL,
            "type": "png",
            "return_type": "base64",
        },
    },
    {
        "name": "html_to_jpeg_binary",
        "params": {
            "url": URL,
            "type": "jpeg",
            "return_type": "binary",
        },
    },
    {
        "name": "html_string_to_pdf",
        "params": {
            "html": "<html><body><h1>Test Document</h1><p>This is a test.</p></body></html>",
            "type": "pdf",
            "return_type": "url",
        },
    },
    {
        "name": "html_to_pdf_with_options",
        "params": {
            "url": URL,
            "type": "pdf",
            "return_type": "url",
            "pdf_display_header_footer": True,
            "pdf_print_background": True,
        },
    },
    {
        "name": "html_to_png_full_page",
        "params": {
            "url": URL,
            "type": "png",
            "full_page": True,
            "return_type": "url",
        },
    },
    {
        "name": "html_to_webp_custom_size",
        "params": {
            "url": URL,
            "type": "webp",
            "width": 1920,
            "height": 1080,
            "return_type": "base64",
        },
    },
    {
        "name": "html_to_png_mobile",
        "params": {
            "url": URL,
            "type": "png",
            "is_mobile": True,
            "return_type": "url",
        },
    },
    {
        "name": "html_to_png_dark_mode",
        "params": {
            "url": URL,
            "type": "png",
            "dark_mode": True,
            "return_type": "url",
        },
    },
]

# Search Test Cases
SEARCH_TEST_CASES = [
    {
        "name": "basic_search",
        "params": {
            "query": "artificial intelligence news",
        },
    },
    {
        "name": "search_specific_site",
        "params": {
            "query": "documentation site:github.com",
        },
    },
    {
        "name": "search_ai_mode",
        "params": {
            "query": "explain quantum computing",
            "ai_overview": True,
        },
    },
]

# Search Suggestions Test Cases
SEARCH_SUGGESTIONS_TEST_CASES = [
    {
        "name": "basic_suggestions",
        "params": {
            "query": "machine learn",
        },
    },
    {
        "name": "programming_suggestions",
        "params": {
            "query": "python tutor",
        },
    },
    {
        "name": "partial_query_suggestions",
        "params": {
            "query": "artifi",
        },
    },
]


class TestHTMLToAnySync:
    """Test synchronous HTML to Any methods"""

    @pytest.mark.parametrize(
        "test_case",
        HTML_TO_ANY_TEST_CASES,
        ids=[tc["name"] for tc in HTML_TO_ANY_TEST_CASES],
    )
    def test_html_to_any(self, test_case):
        """Test synchronous HTML to Any with various inputs"""
        try:
            result = jigsaw.web.html_to_any(test_case["params"])

            return_type = test_case["params"].get("return_type", "url")

            if return_type == "binary":
                assert isinstance(result, bytes)
                assert len(result) > 0
            else:
                assert result["success"]
                assert "url" in result
                assert isinstance(result["url"], str)

                if return_type == "base64":
                    # Check if it's a valid base64 string
                    assert result["url"].startswith("data:")

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSearchSync:
    """Test synchronous search methods"""

    @pytest.mark.parametrize(
        "test_case", SEARCH_TEST_CASES, ids=[tc["name"] for tc in SEARCH_TEST_CASES]
    )
    def test_search(self, test_case):
        """Test synchronous search with various inputs"""
        try:
            result = jigsaw.web.search(test_case["params"])

            assert result["success"]
            assert "results" in result
            assert isinstance(result["results"], list)

            if test_case["params"].get("max_results"):
                assert len(result["results"]) <= test_case["params"]["max_results"]

            # Check result structure
            for item in result["results"]:
                assert "title" in item
                assert "url" in item
                assert "description" in item

            # Check AI mode response
            if test_case["params"].get("ai"):
                assert "ai_overview" in result

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSearchSuggestionsSync:
    """Test synchronous search suggestions methods"""

    @pytest.mark.parametrize(
        "test_case",
        SEARCH_SUGGESTIONS_TEST_CASES,
        ids=[tc["name"] for tc in SEARCH_SUGGESTIONS_TEST_CASES],
    )
    def test_search_suggestions(self, test_case):
        """Test synchronous search suggestions with various inputs"""
        try:
            result = jigsaw.web.search_suggestions(test_case["params"])

            assert result["success"]
            assert "suggestions" in result
            assert isinstance(result["suggestions"], list)
            assert len(result["suggestions"]) > 0

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


# Async Test Classes


class TestHTMLToAnyAsync:
    """Test asynchronous HTML to Any methods"""

    @pytest.mark.parametrize(
        "test_case",
        HTML_TO_ANY_TEST_CASES,
        ids=[tc["name"] for tc in HTML_TO_ANY_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_html_to_any_async(self, test_case):
        """Test asynchronous HTML to Any with various inputs"""
        try:
            result = await async_jigsaw.web.html_to_any(test_case["params"])

            return_type = test_case["params"].get("return_type", "url")

            if return_type == "binary":
                assert isinstance(result, bytes)
                assert len(result) > 0
            else:
                assert result["success"]
                assert "url" in result
                assert isinstance(result["url"], str)

                if return_type == "base64":
                    # Check if it's a valid base64 string
                    assert result["url"].startswith("data:")

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSearchAsync:
    """Test asynchronous search methods"""

    @pytest.mark.parametrize(
        "test_case", SEARCH_TEST_CASES, ids=[tc["name"] for tc in SEARCH_TEST_CASES]
    )
    @pytest.mark.asyncio
    async def test_search_async(self, test_case):
        """Test asynchronous search with various inputs"""
        try:
            result = await async_jigsaw.web.search(test_case["params"])

            assert result["success"]
            assert "results" in result
            assert isinstance(result["results"], list)

            if test_case["params"].get("max_results"):
                assert len(result["results"]) <= test_case["params"]["max_results"]

            # Check result structure
            for item in result["results"]:
                assert "title" in item
                assert "url" in item
                assert "description" in item

            # Check AI mode response
            if test_case["params"].get("ai_overview"):
                assert "ai_overview" in result

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSearchSuggestionsAsync:
    """Test asynchronous search suggestions methods"""

    @pytest.mark.parametrize(
        "test_case",
        SEARCH_SUGGESTIONS_TEST_CASES,
        ids=[tc["name"] for tc in SEARCH_SUGGESTIONS_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_search_suggestions_async(self, test_case):
        """Test asynchronous search suggestions with various inputs"""
        try:
            result = await async_jigsaw.web.search_suggestions(test_case["params"])

            assert result["success"]
            assert "suggestions" in result
            assert isinstance(result["suggestions"], list)
            assert len(result["suggestions"]) > 0

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
