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

# Sample URLs for NSFW testing
SAFE_IMAGE_URL = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2070"
POTENTIALLY_NSFW_URL = "https://images.unsplash.com/photo-1512310604669-443f26c35f52?q=80&w=868&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

# Profanity Test Cases
PROFANITY_TEST_CASES = [
    {
        "name": "clean_text",
        "params": {"text": "This is a perfectly clean and professional message."},
    },
    {
        "name": "text_with_profanity",
        "params": {
            "text": "This fucking thing is not working properly.",
            "censor_replacement": "****",
        },
    },
    {
        "name": "text_with_custom_censor",
        "params": {
            "text": "What the fuck is going on here?",
            "censor_replacement": "[CENSORED]",
        },
    },
    {
        "name": "mixed_clean_and_profane",
        "params": {"text": "The weather is nice but this damn traffic is terrible."},
    },
    {
        "name": "no_censor_replacement",
        "params": {"text": "This text might contain some inappropriate words."},
    },
]

# NSFW Test Cases
NSFW_TEST_CASES = [
    {
        "name": "safe_image_url",
        "params": {"url": SAFE_IMAGE_URL},
    },
    {
        "name": "landscape_image_url",
        "params": {"url": POTENTIALLY_NSFW_URL},
    },
]

# NSFW Blob Test Cases
NSFW_BLOB_TEST_CASES = [
    {
        "name": "safe_image_blob",
        "blob_url": SAFE_IMAGE_URL,
        "options": {},
    },
]


class TestProfanitySync:
    """Test synchronous profanity check methods"""

    @pytest.mark.parametrize(
        "test_case",
        PROFANITY_TEST_CASES,
        ids=[tc["name"] for tc in PROFANITY_TEST_CASES],
    )
    def test_profanity_check(self, test_case):
        """Test synchronous profanity check with various inputs"""
        try:
            result = jigsaw.validate.profanity(test_case["params"])

            assert result["success"]
            assert "clean_text" in result
            assert "profanities" in result
            assert "profanities_found" in result
            assert isinstance(result["profanities_found"], bool)
            assert isinstance(result["profanities"], list)
            assert isinstance(result["clean_text"], str)

            # Check profanities structure
            for profanity in result["profanities"]:
                assert "profanity" in profanity
                assert "startIndex" in profanity
                assert "endIndex" in profanity

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestNSFWSync:
    """Test synchronous NSFW check methods"""

    @pytest.mark.parametrize(
        "test_case", NSFW_TEST_CASES, ids=[tc["name"] for tc in NSFW_TEST_CASES]
    )
    def test_nsfw_check(self, test_case):
        """Test synchronous NSFW check with various inputs"""
        try:
            result = jigsaw.validate.nsfw(test_case["params"])

            assert result["success"]
            assert "nsfw" in result
            assert "nudity" in result
            assert "gore" in result
            assert "nsfw_score" in result
            assert "nudity_score" in result
            assert "gore_score" in result

            assert isinstance(result["nsfw"], bool)
            assert isinstance(result["nudity"], bool)
            assert isinstance(result["gore"], bool)
            assert 0 <= result["nsfw_score"] <= 1
            assert 0 <= result["nudity_score"] <= 1
            assert 0 <= result["gore_score"] <= 1

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case",
        NSFW_BLOB_TEST_CASES,
        ids=[tc["name"] for tc in NSFW_BLOB_TEST_CASES],
    )
    def test_nsfw_check_blob(self, test_case):
        """Test synchronous NSFW check with blob inputs"""
        try:
            # Download blob content
            blob_content = requests.get(test_case["blob_url"]).content
            result = jigsaw.validate.nsfw(blob_content, test_case["options"])

            assert result["success"]
            assert "nsfw" in result
            assert "nudity" in result
            assert "gore" in result
            assert "nsfw_score" in result
            assert "nudity_score" in result
            assert "gore_score" in result

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


# Async Test Classes


class TestProfanityAsync:
    """Test asynchronous profanity check methods"""

    @pytest.mark.parametrize(
        "test_case",
        PROFANITY_TEST_CASES,
        ids=[tc["name"] for tc in PROFANITY_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_profanity_check_async(self, test_case):
        """Test asynchronous profanity check with various inputs"""
        try:
            result = await async_jigsaw.validate.profanity(test_case["params"])

            assert result["success"]
            assert "clean_text" in result
            assert "profanities" in result
            assert "profanities_found" in result
            assert isinstance(result["profanities_found"], bool)
            assert isinstance(result["profanities"], list)
            assert isinstance(result["clean_text"], str)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestNSFWAsync:
    """Test asynchronous NSFW check methods"""

    @pytest.mark.parametrize(
        "test_case", NSFW_TEST_CASES, ids=[tc["name"] for tc in NSFW_TEST_CASES]
    )
    @pytest.mark.asyncio
    async def test_nsfw_check_async(self, test_case):
        """Test asynchronous NSFW check with various inputs"""
        try:
            result = await async_jigsaw.validate.nsfw(test_case["params"])

            assert result["success"]
            assert "nsfw" in result
            assert "nudity" in result
            assert "gore" in result
            assert "nsfw_score" in result
            assert "nudity_score" in result
            assert "gore_score" in result

            assert isinstance(result["nsfw"], bool)
            assert isinstance(result["nudity"], bool)
            assert isinstance(result["gore"], bool)
            assert 0 <= result["nsfw_score"] <= 1
            assert 0 <= result["nudity_score"] <= 1
            assert 0 <= result["gore_score"] <= 1

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case",
        NSFW_BLOB_TEST_CASES,
        ids=[tc["name"] for tc in NSFW_BLOB_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_nsfw_check_blob_async(self, test_case):
        """Test asynchronous NSFW check with blob inputs"""
        try:
            # Download blob content
            blob_content = requests.get(test_case["blob_url"]).content
            result = await async_jigsaw.validate.nsfw(blob_content, test_case["options"])

            assert result["success"]
            assert "nsfw" in result
            assert "nudity" in result
            assert "gore" in result
            assert "nsfw_score" in result
            assert "nudity_score" in result
            assert "gore_score" in result

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
