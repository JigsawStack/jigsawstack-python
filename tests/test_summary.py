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

LONG_TEXT = """
Artificial Intelligence (AI) has become one of the most transformative technologies of the 21st century.
From healthcare to finance, transportation to entertainment, AI is reshaping industries and changing the way we live and work.
Machine learning algorithms can now diagnose diseases with remarkable accuracy, predict market trends, and even create art.
Natural language processing has enabled computers to understand and generate human language, leading to the development of sophisticated chatbots and virtual assistants.
Computer vision systems can identify objects, faces, and activities in images and videos with superhuman precision.
However, the rapid advancement of AI also raises important ethical questions about privacy, job displacement, and the potential for bias in algorithmic decision-making.
As we continue to develop more powerful AI systems, it's crucial that we consider their societal impact and work to ensure that the benefits of AI are distributed equitably.
The future of AI holds immense promise, but it will require careful planning, regulation, and collaboration between technologists, policymakers, and society at large to realize its full potential while mitigating its risks.
"""

ARTICLE_URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"
PDF_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

TEST_CASES = [
    {
        "name": "text_summary_default",
        "params": {
            "text": LONG_TEXT,
        },
    },
    {
        "name": "text_summary_with_text_type",
        "params": {
            "text": LONG_TEXT,
            "type": "text",
        },
    },
    {
        "name": "text_summary_with_points_type",
        "params": {
            "text": LONG_TEXT,
            "type": "points",
        },
    },
    {
        "name": "text_summary_with_max_points",
        "params": {
            "text": LONG_TEXT,
            "type": "points",
            "max_points": 5,
        },
    },
    {
        "name": "text_summary_with_max_characters",
        "params": {
            "text": LONG_TEXT,
            "type": "text",
            "max_characters": 200,
        },
    },
    {
        "name": "short_text_summary",
        "params": {
            "text": "This is a short text that doesn't need much summarization.",
        },
    },
    {
        "name": "url_summary_default",
        "params": {
            "url": ARTICLE_URL,
        },
    },
    {
        "name": "url_summary_with_text_type",
        "params": {
            "url": ARTICLE_URL,
            "type": "text",
        },
    },
    {
        "name": "url_summary_with_points_type",
        "params": {
            "url": ARTICLE_URL,
            "type": "points",
            "max_points": 7,
        },
    },
    {
        "name": "pdf_url_summary",
        "params": {
            "url": PDF_URL,
            "type": "text",
        },
    },
    {
        "name": "complex_text_with_points_and_limit",
        "params": {
            "text": LONG_TEXT * 3,  # Triple the text for more content
            "type": "points",
            "max_points": 10,
        },
    },
    {
        "name": "technical_text_summary",
        "params": {
            "text": """
            Machine learning is a subset of artificial intelligence that focuses on the development of algorithms and statistical models that enable computer systems to improve their performance on a specific task through experience.
            Deep learning, a subfield of machine learning, uses artificial neural networks with multiple layers to progressively extract higher-level features from raw input.
            Supervised learning involves training models on labeled data, while unsupervised learning discovers patterns in unlabeled data.
            Reinforcement learning enables agents to learn optimal behaviors through trial and error interactions with an environment.
            """,
            "type": "points",
            "max_points": 4,
        },
    },
]


class TestSummarySync:
    """Test synchronous summary methods"""

    sync_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_summary(self, test_case):
        """Test synchronous summary with various inputs"""
        try:
            result = jigsaw.summary(test_case["params"])

            assert result["success"]
            assert "summary" in result

            if test_case["params"].get("type") == "points":
                assert isinstance(result["summary"], list)
                if "max_points" in test_case["params"]:
                    assert len(result["summary"]) <= test_case["params"]["max_points"]
            else:
                assert isinstance(result["summary"], str)
                if "max_characters" in test_case["params"]:
                    assert (
                        len(result["summary"]) <= test_case["params"]["max_characters"]
                    )

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSummaryAsync:
    """Test asynchronous summary methods"""

    async_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_summary_async(self, test_case):
        """Test asynchronous summary with various inputs"""
        try:
            result = await async_jigsaw.summary(test_case["params"])

            assert result["success"]
            assert "summary" in result

            if test_case["params"].get("type") == "points":
                assert isinstance(result["summary"], list)
                if "max_points" in test_case["params"]:
                    assert len(result["summary"]) <= test_case["params"]["max_points"]
            else:
                assert isinstance(result["summary"], str)
                if "max_characters" in test_case["params"]:
                    assert (
                        len(result["summary"]) <= test_case["params"]["max_characters"]
                    )

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
