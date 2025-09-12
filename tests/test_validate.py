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

jigsaw = jigsawstack.JigsawStack(
    api_url="http://localhost:3000/api/", api_key=os.getenv("JIGSAWSTACK_API_KEY")
)
async_jigsaw = jigsawstack.AsyncJigsawStack(
    api_url="http://localhost:3000/api/", api_key=os.getenv("JIGSAWSTACK_API_KEY")
)

# Sample URLs for NSFW testing
SAFE_IMAGE_URL = (
    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=2070"
)
POTENTIALLY_NSFW_URL = "https://images.unsplash.com/photo-1512310604669-443f26c35f52?q=80&w=868&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

SPAM_CHECK_TEST_CASES = [
    {
        "name": "single_text_not_spam",
        "params": {
            "text": "I had a great experience with your product. The customer service was excellent!"
        },
    },
    {
        "name": "single_text_potential_spam",
        "params": {
            "text": "CLICK HERE NOW!!! FREE MONEY!!! Win $1000000 instantly! No credit card required! Act NOW!"
        },
    },
    {
        "name": "multiple_texts_mixed",
        "params": {
            "text": [
                "Thank you for your email. I'll get back to you soon.",
                "BUY NOW! LIMITED TIME OFFER! 90% OFF EVERYTHING!",
                "The meeting is scheduled for 3 PM tomorrow.",
            ]
        },
    },
    {
        "name": "professional_email",
        "params": {
            "text": "Dear John, I hope this email finds you well. I wanted to follow up on our discussion from yesterday."
        },
    },
    {
        "name": "marketing_spam",
        "params": {
            "text": "Congratulations! You've been selected as our lucky winner! Claim your prize now at this link: bit.ly/win"
        },
    },
]

# Spell Check Test Cases
SPELL_CHECK_TEST_CASES = [
    {
        "name": "text_with_no_errors",
        "params": {"text": "The quick brown fox jumps over the lazy dog."},
    },
    {
        "name": "text_with_spelling_errors",
        "params": {"text": "Thiss sentense has severel speling erors in it."},
    },
    {
        "name": "text_with_language_code",
        "params": {"text": "I recieved the pacakge yesterday.", "language_code": "en"},
    },
    {
        "name": "mixed_correct_and_incorrect",
        "params": {
            "text": "The weather is beatiful today, but tommorow might be diferent."
        },
    },
    {
        "name": "technical_text",
        "params": {"text": "The algorythm processes the datbase queries eficiently."},
    },
]

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


class TestSpamCheckSync:
    """Test synchronous spam check methods"""

    @pytest.mark.parametrize(
        "test_case",
        SPAM_CHECK_TEST_CASES,
        ids=[tc["name"] for tc in SPAM_CHECK_TEST_CASES],
    )
    def test_spam_check(self, test_case):
        """Test synchronous spam check with various inputs"""
        try:
            result = jigsaw.validate.spamcheck(test_case["params"])

            assert result["success"]
            assert "check" in result

            # Check structure based on input type
            if isinstance(test_case["params"]["text"], list):
                assert isinstance(result["check"], list)
                for check in result["check"]:
                    assert "is_spam" in check
                    assert "score" in check
                    assert isinstance(check["is_spam"], bool)
                    assert 0 <= check["score"] <= 1
            else:
                assert "is_spam" in result["check"]
                assert "score" in result["check"]
                assert isinstance(result["check"]["is_spam"], bool)
                assert 0 <= result["check"]["score"] <= 1

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSpellCheckSync:
    """Test synchronous spell check methods"""

    @pytest.mark.parametrize(
        "test_case",
        SPELL_CHECK_TEST_CASES,
        ids=[tc["name"] for tc in SPELL_CHECK_TEST_CASES],
    )
    def test_spell_check(self, test_case):
        """Test synchronous spell check with various inputs"""
        try:
            result = jigsaw.validate.spellcheck(test_case["params"])

            assert result["success"]
            assert "misspellings_found" in result
            assert "misspellings" in result
            assert "auto_correct_text" in result
            assert isinstance(result["misspellings_found"], bool)
            assert isinstance(result["misspellings"], list)
            assert isinstance(result["auto_correct_text"], str)

            # Check misspellings structure
            for misspelling in result["misspellings"]:
                assert "word" in misspelling
                assert "startIndex" in misspelling
                assert "endIndex" in misspelling
                assert "expected" in misspelling
                assert "auto_corrected" in misspelling
                assert isinstance(misspelling["expected"], list)
                assert isinstance(misspelling["auto_corrected"], bool)

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


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


class TestSpamCheckAsync:
    """Test asynchronous spam check methods"""

    @pytest.mark.parametrize(
        "test_case",
        SPAM_CHECK_TEST_CASES,
        ids=[tc["name"] for tc in SPAM_CHECK_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_spam_check_async(self, test_case):
        """Test asynchronous spam check with various inputs"""
        try:
            result = await async_jigsaw.validate.spamcheck(test_case["params"])

            assert result["success"]
            assert "check" in result

            # Check structure based on input type
            if isinstance(test_case["params"]["text"], list):
                assert isinstance(result["check"], list)
                for check in result["check"]:
                    assert "is_spam" in check
                    assert "score" in check
                    assert isinstance(check["is_spam"], bool)
                    assert 0 <= check["score"] <= 1
            else:
                assert "is_spam" in result["check"]
                assert "score" in result["check"]
                assert isinstance(result["check"]["is_spam"], bool)
                assert 0 <= result["check"]["score"] <= 1

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSpellCheckAsync:
    """Test asynchronous spell check methods"""

    @pytest.mark.parametrize(
        "test_case",
        SPELL_CHECK_TEST_CASES,
        ids=[tc["name"] for tc in SPELL_CHECK_TEST_CASES],
    )
    @pytest.mark.asyncio
    async def test_spell_check_async(self, test_case):
        """Test asynchronous spell check with various inputs"""
        try:
            result = await async_jigsaw.validate.spellcheck(test_case["params"])

            assert result["success"]
            assert "misspellings_found" in result
            assert "misspellings" in result
            assert "auto_correct_text" in result
            assert isinstance(result["misspellings_found"], bool)
            assert isinstance(result["misspellings"], list)
            assert isinstance(result["auto_correct_text"], str)

            # Check misspellings structure
            for misspelling in result["misspellings"]:
                assert "word" in misspelling
                assert "startIndex" in misspelling
                assert "endIndex" in misspelling
                assert "expected" in misspelling
                assert "auto_corrected" in misspelling

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


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
            result = await async_jigsaw.validate.nsfw(
                blob_content, test_case["options"]
            )

            assert result["success"]
            assert "nsfw" in result
            assert "nudity" in result
            assert "gore" in result
            assert "nsfw_score" in result
            assert "nudity_score" in result
            assert "gore_score" in result

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
