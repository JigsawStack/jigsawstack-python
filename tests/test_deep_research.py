import logging
import os

import pytest
from dotenv import load_dotenv

import jigsawstack
from jigsawstack.exceptions import JigsawStackError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


# Deep Research Test Cases
DEEP_RESEARCH_TEST_CASES = [
    {
        "name": "basic_deep_research",
        "params": {
            "query": "climate change effects",
        },
    },
    {
        "name": "technical_deep_research",
        "params": {
            "query": "quantum computing applications in cryptography",
        },
    },
    {
        "name": "deep_research_with_depth",
        "params": {
            "query": "renewable energy sources",
            "depth": 2,
        },
    },
]


class TestDeepResearchSync:
    """Test synchronous deep research methods"""

    @pytest.mark.parametrize(
        "test_case",
        DEEP_RESEARCH_TEST_CASES,
        ids=[tc["name"] for tc in DEEP_RESEARCH_TEST_CASES],
    )
    def test_deep_research(self, test_case):
        """Test synchronous deep research with various inputs"""
        try:
            result = jigsaw.web.deep_research(test_case["params"])

            assert result["success"]
            assert "results" in result
            assert isinstance(result["results"], str)
            assert len(result["results"]) > 0

            # Check for sources
            if "sources" in result:
                assert isinstance(result["sources"], list)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestDeepResearchAsync:
    """Test asynchronous deep research methods"""

    @pytest.mark.parametrize(
        "test_case",
        DEEP_RESEARCH_TEST_CASES,
        ids=[tc["name"] for tc in DEEP_RESEARCH_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_deep_research_async(self, test_case):
        """Test asynchronous deep research with various inputs"""
        try:
            result = await async_jigsaw.web.deep_research(test_case["params"])

            assert result["success"]
            assert "results" in result
            assert isinstance(result["results"], str)
            assert len(result["results"]) > 0

            # Check for sources
            if "sources" in result:
                assert isinstance(result["sources"], list)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
