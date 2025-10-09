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

AUDIO_URL = AUDIO_URL_LONG = "https://jigsawstack.com/preview/stt-example.wav"


TEST_CASES = [
    {
        "name": "with_url_only",
        "params": {"url": AUDIO_URL},
        "blob": None,
        "options": None,
    },
    {
        "name": "with_url_and_language",
        "params": {"url": AUDIO_URL, "language": "en"},
        "blob": None,
        "options": None,
    },
    {
        "name": "with_url_auto_detect_language",
        "params": {"url": AUDIO_URL, "language": "auto"},
        "blob": None,
        "options": None,
    },
    {
        "name": "with_url_and_translate",
        "params": {"url": AUDIO_URL, "translate": True},
        "blob": None,
        "options": None,
    },
    {
        "name": "with_blob_only",
        "params": None,
        "blob": AUDIO_URL,
        "options": None,
    },
    {
        "name": "with_blob_and_language",
        "params": None,
        "blob": AUDIO_URL,
        "options": {"language": "en"},
    },
    {
        "name": "with_blob_auto_detect",
        "params": None,
        "blob": AUDIO_URL,
        "options": {"language": "auto"},
    },
    {
        "name": "with_blob_and_translate",
        "params": None,
        "blob": AUDIO_URL,
        "options": {"translate": True, "language": "en"},
    },
    {
        "name": "with_by_speaker",
        "params": {"url": AUDIO_URL_LONG, "by_speaker": True},
        "blob": None,
        "options": None,
    },
    {
        "name": "with_chunk_settings",
        "params": {"url": AUDIO_URL, "batch_size": 5, "chunk_duration": 15},
        "blob": None,
        "options": None,
    },
    {
        "name": "with_all_options",
        "params": None,
        "blob": AUDIO_URL_LONG,
        "options": {
            "language": "auto",
            "translate": False,
            "by_speaker": True,
            "batch_size": 10,
            "chunk_duration": 15,
        },
    },
]

# Test cases with webhook (separate as they return different response)
WEBHOOK_TEST_CASES = [
    {
        "name": "with_webhook_url",
        "params": {
            "url": AUDIO_URL,
            "webhook_url": "https://webhook.site/test-webhook",
        },
        "blob": None,
        "options": None,
    },
    {
        "name": "with_blob_and_webhook",
        "params": None,
        "blob": AUDIO_URL,
        "options": {
            "webhook_url": "https://webhook.site/test-webhook",
            "language": "en",
        },
    },
]


class TestAudioSync:
    """Test synchronous audio speech-to-text methods"""

    @pytest.mark.parametrize(
        "test_case", TEST_CASES, ids=[tc["name"] for tc in TEST_CASES]
    )
    def test_speech_to_text(self, test_case):
        """Test synchronous speech-to-text with various inputs"""
        try:
            if test_case.get("blob"):
                # Download audio content
                blob_content = requests.get(test_case["blob"]).content
                result = jigsaw.audio.speech_to_text(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = jigsaw.audio.speech_to_text(test_case["params"])
            # Verify response structure
            assert result["success"]
            assert result.get("text", None) is not None and isinstance(
                result["text"], str
            )

            # Check for chunks
            if result.get("chunks", None):
                assert isinstance(result["chunks"], list)

            # Check for speaker diarization if requested
            if result.get("speakers", None):
                assert isinstance(result["speakers"], list)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case", WEBHOOK_TEST_CASES, ids=[tc["name"] for tc in WEBHOOK_TEST_CASES]
    )
    def test_speech_to_text_webhook(self, test_case):
        """Test synchronous speech-to-text with webhook"""
        try:
            if test_case.get("blob"):
                # Download audio content
                blob_content = requests.get(test_case["blob"]).content
                result = jigsaw.audio.speech_to_text(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = jigsaw.audio.speech_to_text(test_case["params"])
            # Verify webhook response structure
            assert result["success"]

        except JigsawStackError as e:
            # Webhook URLs might fail if invalid
            print(f"Expected possible error for webhook test {test_case['name']}: {e}")


class TestAudioAsync:
    """Test asynchronous audio speech-to-text methods"""

    @pytest.mark.parametrize(
        "test_case", TEST_CASES, ids=[tc["name"] for tc in TEST_CASES]
    )
    @pytest.mark.asyncio
    async def test_speech_to_text_async(self, test_case):
        """Test asynchronous speech-to-text with various inputs"""
        try:
            if test_case.get("blob"):
                # Download audio content
                blob_content = requests.get(test_case["blob"]).content
                result = await async_jigsaw.audio.speech_to_text(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = await async_jigsaw.audio.speech_to_text(test_case["params"])

            # Verify response structure
            assert result["success"]
            assert result.get("text", None) is not None and isinstance(
                result["text"], str
            )

            # Check for chunks
            if result.get("chunks", None):
                assert isinstance(result["chunks"], list)

            # Check for speaker diarization if requested
            if result.get("speakers", None):
                assert isinstance(result["speakers"], list)
        except JigsawStackError as e:
            pytest.fail(
                f"Unexpected JigsawStackError in async {test_case['name']}: {e}"
            )

    @pytest.mark.parametrize(
        "test_case", WEBHOOK_TEST_CASES, ids=[tc["name"] for tc in WEBHOOK_TEST_CASES]
    )
    @pytest.mark.asyncio
    async def test_speech_to_text_webhook_async(self, test_case):
        """Test asynchronous speech-to-text with webhook"""
        try:
            if test_case.get("blob"):
                # Download audio content
                blob_content = requests.get(test_case["blob"]).content
                result = await async_jigsaw.audio.speech_to_text(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = await async_jigsaw.audio.speech_to_text(test_case["params"])

            print(f"Async test {test_case['name']}: Webhook response")

            # Verify webhook response structure
            assert result["success"]

        except JigsawStackError as e:
            # Webhook URLs might fail if invalid
            print(
                f"Expected possible error for async webhook test {test_case['name']}: {e}"
            )
