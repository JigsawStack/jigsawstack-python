import logging
import os

import pytest
import requests
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

IMAGE_URL = "https://jigsawstack.com/preview/vocr-example.jpg"

# PDF URL for testing page_range functionality
PDF_URL = "https://arxiv.org/pdf/1706.03762"

TEST_CASES = [
    {
        "name": "with_url_only",
        "params": {"url": IMAGE_URL},
        "blob": None,
        "options": None,
    },
    {
        "name": "with_blob_only",
        "params": None,
        "blob": IMAGE_URL,
        "options": None,
    },
    {
        "name": "with_string_prompt",
        "blob": IMAGE_URL,
        "options": {"prompt": "Extract all text from the image"},
    },
    {
        "name": "with_list_prompt",
        "blob": IMAGE_URL,
        "options": {
            "prompt": [
                "What is the main heading?",
                "Extract any dates mentioned",
                "What are the key points?",
            ]
        },
    },
    {
        "name": "with_dict_prompt",
        "blob": IMAGE_URL,
        "options": {
            "prompt": {
                "title": "Extract the main title",
                "content": "What is the main content?",
                "metadata": "Extract any metadata or additional information",
            }
        },
    },
    {
        "name": "url_with_string_prompt",
        "params": {"url": IMAGE_URL, "prompt": "Summarize the text content"},
        "blob": None,
        "options": None,
    },
    {
        "name": "url_with_list_prompt",
        "params": {
            "url": IMAGE_URL,
            "prompt": ["Extract headers", "Extract body text"],
        },
        "blob": None,
        "options": None,
    },
]

# PDF specific test cases
PDF_TEST_CASES = [
    {
        "name": "pdf_with_page_range",
        "params": {
            "url": PDF_URL,
            "page_range": [1, 3],
            "prompt": "Extract text from these pages",
        },
        "blob": None,
        "options": None,
    },
    {
        "name": "pdf_single_page",
        "params": {
            "url": PDF_URL,
            "page_range": [1, 1],
            "prompt": "What is on the first page?",
        },
        "blob": None,
        "options": None,
    },
    {
        "name": "pdf_blob_with_page_range",
        "blob": PDF_URL,
        "options": {"page_range": [1, 3], "prompt": "what is this about?"},
    },
]


class TestVOCRSync:
    """Test synchronous VOCR methods"""

    sync_test_cases = TEST_CASES
    pdf_test_cases = PDF_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_vocr(self, test_case):
        """Test synchronous VOCR with various inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = jigsaw.vision.vocr(blob_content, test_case.get("options", {}))
            else:
                # Use params directly
                result = jigsaw.vision.vocr(test_case["params"])

            print(f"Test {test_case['name']}: Success={result.get('success')}")

            # Verify response structure
            assert result["success"] is True
            if "prompt" in (test_case.get("params") or {}):
                assert "context" in result
            assert "width" in result
            assert "height" in result
            assert "has_text" in result
            assert "tags" in result
            assert isinstance(result["tags"], list)
            assert "sections" in result
            assert isinstance(result["sections"], list)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case", pdf_test_cases, ids=[tc["name"] for tc in pdf_test_cases]
    )
    def test_vocr_pdf(self, test_case):
        """Test synchronous VOCR with PDF inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = jigsaw.vision.vocr(blob_content, test_case.get("options", {}))
            else:
                # Use params directly
                result = jigsaw.vision.vocr(test_case["params"])

            # Verify response structure
            assert result["success"] is True
            if "prompt" in (test_case.get("params") or {}):
                assert "context" in result
            assert "total_pages" in result

            if test_case.get("params", {}).get("page_range") or test_case.get(
                "options", {}
            ).get("page_range"):
                assert "page_range" in result
                assert isinstance(result["page_range"], list)

            logger.info(
                f"Test {test_case['name']}: total_pages={result.get('total_pages')}"
            )

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestVOCRAsync:
    """Test asynchronous VOCR methods"""

    async_test_cases = TEST_CASES
    pdf_test_cases = PDF_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_vocr_async(self, test_case):
        """Test asynchronous VOCR with various inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = await async_jigsaw.vision.vocr(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = await async_jigsaw.vision.vocr(test_case["params"])

            print(f"Test {test_case['name']}: Success={result.get('success')}")

            # Verify response structure
            assert result["success"] is True
            if "prompt" in (test_case.get("params") or {}):
                assert "context" in result
            assert "width" in result
            assert "height" in result
            assert "has_text" in result
            assert "tags" in result
            assert isinstance(result["tags"], list)
            assert "sections" in result
            assert isinstance(result["sections"], list)

            # Log some details
            logger.info(
                f"Test {test_case['name']}: has_text={result['has_text']}, tags={result['tags'][:3] if result['tags'] else []}"
            )

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case", pdf_test_cases, ids=[tc["name"] for tc in pdf_test_cases]
    )
    @pytest.mark.asyncio
    async def test_vocr_pdf_async(self, test_case):
        """Test asynchronous VOCR with PDF inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = await async_jigsaw.vision.vocr(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = await async_jigsaw.vision.vocr(test_case["params"])

            print(f"Test {test_case['name']}: Success={result.get('success')}")

            # Verify response structure
            assert result["success"] is True
            if "prompt" in (test_case.get("params") or {}):
                assert "context" in result
            assert "total_pages" in result  # PDF specific

            # Check if page_range is in response when requested
            if test_case.get("params", {}).get("page_range") or test_case.get(
                "options", {}
            ).get("page_range"):
                assert "page_range" in result
                assert isinstance(result["page_range"], list)

            logger.info(
                f"Test {test_case['name']}: total_pages={result.get('total_pages')}"
            )

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
