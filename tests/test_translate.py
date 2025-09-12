import requests
from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))

# Sample image URL for translation tests
IMAGE_URL = "https://images.unsplash.com/photo-1580679137870-86ef9f9a03d6?q=80&w=2574&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

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

# Image translation test cases
IMAGE_TEST_CASES = [
    {
        "name": "translate_image_with_url",
        "params": {
            "url": IMAGE_URL,
            "target_language": "es",
        },
        "blob": None,
        "options": None,
    },
    {
        "name": "translate_image_with_blob",
        "params": None,
        "blob": IMAGE_URL,
        "options": {
            "target_language": "fr",
        },
    },
    {
        "name": "translate_image_with_url_return_base64",
        "params": {
            "url": IMAGE_URL,
            "target_language": "de",
            "return_type": "base64",
        },
        "blob": None,
        "options": None,
    },
    {
        "name": "translate_image_with_blob_return_url",
        "params": None,
        "blob": IMAGE_URL,
        "options": {
            "target_language": "ja",
            "return_type": "url",
        },
    },
    {
        "name": "translate_image_with_blob_return_binary",
        "params": None,
        "blob": IMAGE_URL,
        "options": {
            "target_language": "zh",
            "return_type": "binary",
        },
    },
    {
        "name": "translate_image_to_italian",
        "params": {
            "url": IMAGE_URL,
            "target_language": "it",
        },
        "blob": None,
        "options": None,
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


class TestTranslateImageSync:
    """Test synchronous image translation methods"""

    sync_test_cases = IMAGE_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_translate_image(self, test_case):
        """Test synchronous image translation with various inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = jigsaw.translate.image(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = jigsaw.translate.image(test_case["params"])
            assert result is not None
            if isinstance(result, dict):
                assert "url" in result
            else:
                assert isinstance(result, bytes)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestTranslateImageAsync:
    """Test asynchronous image translation methods"""

    async_test_cases = IMAGE_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_translate_image_async(self, test_case):
        """Test asynchronous image translation with various inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = await async_jigsaw.translate.image(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = await async_jigsaw.translate.image(test_case["params"])
            assert result is not None
            if isinstance(result, dict):
                assert "url" in result
            else:
                assert isinstance(result, bytes)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")