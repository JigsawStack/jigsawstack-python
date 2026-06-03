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

# Text translation test cases
TEXT_TEST_CASES = [
    {
        "name": "translate_single_text_to_spanish",
        "params": {
            "text": "Hello, how are you?",
            "target_language": "es",
        },
    },
    {
        "name": "translate_single_text_with_current_language",
        "params": {
            "text": "Bonjour, comment allez-vous?",
            "current_language": "fr",
            "target_language": "en",
        },
    },
    {
        "name": "translate_multiple_texts",
        "params": {
            "text": ["Hello world", "Good morning", "Thank you"],
            "target_language": "fr",
        },
    },
    {
        "name": "translate_to_german",
        "params": {
            "text": "The weather is beautiful today",
            "target_language": "de",
        },
    },
    {
        "name": "translate_to_japanese",
        "params": {
            "text": "Welcome to our website",
            "target_language": "ja",
        },
    },
    {
        "name": "translate_multiple_with_source_language",
        "params": {
            "text": ["Ciao", "Grazie", "Arrivederci"],
            "current_language": "it",
            "target_language": "en",
        },
    },
]


class TestTranslateTextSync:
    """Test synchronous text translation methods"""

    sync_test_cases = TEXT_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_translate_text(self, test_case):
        """Test synchronous text translation with various inputs"""
        try:
            result = jigsaw.translate.text(test_case["params"])
            assert result["success"]
            assert "translated_text" in result

            # Check if the response structure matches the input
            if isinstance(test_case["params"]["text"], list):
                assert isinstance(result["translated_text"], list)
                assert len(result["translated_text"]) == len(test_case["params"]["text"])
            else:
                assert isinstance(result["translated_text"], str)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestTranslateTextAsync:
    """Test asynchronous text translation methods"""

    async_test_cases = TEXT_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_translate_text_async(self, test_case):
        """Test asynchronous text translation with various inputs"""
        try:
            result = await async_jigsaw.translate.text(test_case["params"])
            assert result["success"]
            assert "translated_text" in result

            # Check if the response structure matches the input
            if isinstance(test_case["params"]["text"], list):
                assert isinstance(result["translated_text"], list)
                assert len(result["translated_text"]) == len(test_case["params"]["text"])
            else:
                assert isinstance(result["translated_text"], str)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
