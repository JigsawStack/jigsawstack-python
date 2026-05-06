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
