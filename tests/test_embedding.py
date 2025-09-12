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

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))

SAMPLE_TEXT = (
    "The quick brown fox jumps over the lazy dog. This is a sample text for embedding generation."
)
SAMPLE_IMAGE_URL = "https://images.unsplash.com/photo-1542931287-023b922fa89b?q=80&w=2574&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
SAMPLE_AUDIO_URL = "https://jigsawstack.com/preview/stt-example.wav"
SAMPLE_PDF_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# Test cases for Embedding V1
EMBEDDING_V1_TEST_CASES = [
    {
        "name": "text_embedding_basic",
        "params": {
            "type": "text",
            "text": SAMPLE_TEXT,
        },
    },
    {
        "name": "text_embedding_with_truncate",
        "params": {
            "type": "text",
            "text": SAMPLE_TEXT * 100,  # Long text to test truncation
            "token_overflow_mode": "truncate",
        },
    },
    {
        "name": "text_embedding_with_error_mode",
        "params": {
            "type": "text",
            "text": SAMPLE_TEXT,
            "token_overflow_mode": "error",
        },
    },
    {
        "name": "image_embedding_from_url",
        "params": {
            "type": "image",
            "url": SAMPLE_IMAGE_URL,
        },
    },
    {
        "name": "audio_embedding_from_url",
        "params": {
            "type": "audio",
            "url": SAMPLE_AUDIO_URL,
        },
    },
    {
        "name": "pdf_embedding_from_url",
        "params": {
            "type": "pdf",
            "url": SAMPLE_PDF_URL,
        },
    },
    {
        "name": "text_other_type",
        "params": {
            "type": "text-other",
            "text": "This is a different text type for embedding",
        },
    },
]

# Test cases for Embedding V2
EMBEDDING_V2_TEST_CASES = [
    {
        "name": "text_embedding_v2_basic",
        "params": {
            "type": "text",
            "text": SAMPLE_TEXT,
        },
    },
    {
        "name": "text_embedding_v2_with_error",
        "params": {
            "type": "text",
            "text": SAMPLE_TEXT * 100,  # Long text to test chunking
            "token_overflow_mode": "error",
        },
    },
    {
        "name": "text_embedding_v2_with_truncate",
        "params": {
            "type": "text",
            "text": SAMPLE_TEXT * 100,
            "token_overflow_mode": "truncate",
        },
    },
    {
        "name": "text_embedding_v2_with_error_mode",
        "params": {
            "type": "text",
            "text": SAMPLE_TEXT,
            "token_overflow_mode": "error",
        },
    },
    {
        "name": "image_embedding_v2_from_url",
        "params": {
            "type": "image",
            "url": SAMPLE_IMAGE_URL,
        },
    },
    {
        "name": "audio_embedding_v2_basic",
        "params": {
            "type": "audio",
            "url": SAMPLE_AUDIO_URL,
        },
    },
    {
        "name": "audio_embedding_v2_with_speaker_fingerprint",
        "params": {
            "type": "audio",
            "url": SAMPLE_AUDIO_URL,
            "speaker_fingerprint": True,
        },
    },
    {
        "name": "pdf_embedding_v2_from_url",
        "params": {
            "type": "pdf",
            "url": SAMPLE_PDF_URL,
        },
    },
]

# Test cases for blob inputs
BLOB_TEST_CASES = [
    {
        "name": "image_blob_embedding",
        "blob_url": SAMPLE_IMAGE_URL,
        "options": {
            "type": "image",
        },
    },
    {
        "name": "pdf_blob_embedding",
        "blob_url": SAMPLE_PDF_URL,
        "options": {
            "type": "pdf",
        },
    },
]


class TestEmbeddingV1Sync:
    """Test synchronous Embedding V1 methods"""

    sync_test_cases = EMBEDDING_V1_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_embedding_v1(self, test_case):
        """Test synchronous embedding v1 with various inputs"""
        try:
            result = jigsaw.embedding(test_case["params"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)
            if "chunks" in result:
                assert isinstance(result["chunks"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case", BLOB_TEST_CASES, ids=[tc["name"] for tc in BLOB_TEST_CASES]
    )
    def test_embedding_v1_blob(self, test_case):
        """Test synchronous embedding v1 with blob inputs"""
        try:
            # Download blob content
            blob_content = requests.get(test_case["blob_url"]).content
            result = jigsaw.embedding(blob_content, test_case["options"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestEmbeddingV1Async:
    """Test asynchronous Embedding V1 methods"""

    async_test_cases = EMBEDDING_V1_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_embedding_v1_async(self, test_case):
        """Test asynchronous embedding v1 with various inputs"""
        try:
            result = await async_jigsaw.embedding(test_case["params"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)
            if "chunks" in result:
                assert isinstance(result["chunks"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case", BLOB_TEST_CASES, ids=[tc["name"] for tc in BLOB_TEST_CASES]
    )
    @pytest.mark.asyncio
    async def test_embedding_v1_blob_async(self, test_case):
        """Test asynchronous embedding v1 with blob inputs"""
        try:
            # Download blob content
            blob_content = requests.get(test_case["blob_url"]).content
            result = await async_jigsaw.embedding(blob_content, test_case["options"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestEmbeddingV2Sync:
    """Test synchronous Embedding V2 methods"""

    sync_test_cases = EMBEDDING_V2_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_embedding_v2(self, test_case):
        """Test synchronous embedding v2 with various inputs"""
        try:
            result = jigsaw.embeddingV2(test_case["params"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)

            # Check for chunks when chunking mode is used
            if test_case["params"].get("token_overflow_mode") == "error":
                assert "chunks" in result
                assert isinstance(result["chunks"], list)

            # Check for speaker embeddings when speaker fingerprint is requested
            if test_case["params"].get("speaker_fingerprint"):
                assert "speaker_embeddings" in result
                assert isinstance(result["speaker_embeddings"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case", BLOB_TEST_CASES, ids=[tc["name"] for tc in BLOB_TEST_CASES]
    )
    def test_embedding_v2_blob(self, test_case):
        """Test synchronous embedding v2 with blob inputs"""
        try:
            # Download blob content
            blob_content = requests.get(test_case["blob_url"]).content
            result = jigsaw.embeddingV2(blob_content, test_case["options"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestEmbeddingV2Async:
    """Test asynchronous Embedding V2 methods"""

    async_test_cases = EMBEDDING_V2_TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_embedding_v2_async(self, test_case):
        """Test asynchronous embedding v2 with various inputs"""
        try:
            result = await async_jigsaw.embeddingV2(test_case["params"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)

            # Check for chunks when chunking mode is used
            if test_case["params"].get("token_overflow_mode") == "error":
                assert "chunks" in result
                assert isinstance(result["chunks"], list)

            # Check for speaker embeddings when speaker fingerprint is requested
            if test_case["params"].get("speaker_fingerprint"):
                assert "speaker_embeddings" in result
                assert isinstance(result["speaker_embeddings"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")

    @pytest.mark.parametrize(
        "test_case", BLOB_TEST_CASES, ids=[tc["name"] for tc in BLOB_TEST_CASES]
    )
    @pytest.mark.asyncio
    async def test_embedding_v2_blob_async(self, test_case):
        """Test asynchronous embedding v2 with blob inputs"""
        try:
            # Download blob content
            blob_content = requests.get(test_case["blob_url"]).content
            result = await async_jigsaw.embeddingV2(blob_content, test_case["options"])
            assert result["success"]
            assert "embeddings" in result
            assert isinstance(result["embeddings"], list)
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
