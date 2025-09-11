import requests
from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest
import logging
from dotenv import load_dotenv
import os
import uuid

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))

TEXT_FILE_CONTENT = b"This is a test file content for JigsawStack storage"
JSON_FILE_CONTENT = b'{"test": "data", "key": "value"}'
BINARY_FILE_CONTENT = requests.get("https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Collabo%201080x842.jpg").content

TEST_CASES_UPLOAD = [
    {
        "name": "upload_text_file_with_key",
        "file": TEXT_FILE_CONTENT,
        "options": {
            "key": "sample_file.txt",
            "content_type": "text/plain",
            "overwrite": True,
        },
    },
    {
        "name": "upload_image_with_temp_url",
        "file": BINARY_FILE_CONTENT,
        "options": {
            "key": f"test_image.jpg",
            "content_type": "image/jpeg",
            "overwrite": True,
            "temp_public_url": True,
        },
    },
    {
        "name": "upload_binary_file",
        "file": BINARY_FILE_CONTENT,
        "options": {
            "overwrite": True,
        },
    },
    {
        "name": "upload_file_no_options",
        "file": TEXT_FILE_CONTENT,
        "options": None,
    },
]


class TestFileStoreSync:
    """Test synchronous file store operations"""
    
    uploaded_keys = []  # Track uploaded files for cleanup
    
    @pytest.mark.parametrize("test_case", TEST_CASES_UPLOAD, ids=[tc["name"] for tc in TEST_CASES_UPLOAD])
    def test_file_upload(self, test_case):
        """Test synchronous file upload with various options"""
        try:
            result = jigsaw.store.upload(test_case["file"], test_case["options"])
            
            print(f"Upload test {test_case['name']}: {result}")
            assert result.get("key") is not None
            assert result.get("url") is not None
            assert result.get("size") > 0
            
            # Check temp_public_url if requested
            if test_case.get("options") and test_case["options"].get("temp_public_url"):
                assert result.get("temp_public_url") is not None
            
            # Store key for cleanup
            self.uploaded_keys.append(result["key"])
            
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
    
    def test_file_get(self):
        """Test synchronous file retrieval"""
        # First upload a file to retrieve
        test_key = f"test-get-{uuid.uuid4().hex[:8]}.txt"
        try:
            upload_result = jigsaw.store.upload(
                TEXT_FILE_CONTENT,
                {"key": test_key, "content_type": "text/plain"}
            )
            
            # Now retrieve it
            file_content = jigsaw.store.get(upload_result["key"])
            assert file_content is not None
            print(f"Retrieved file with key {upload_result['key']}")
            
            # Cleanup
            self.uploaded_keys.append(upload_result["key"])
            
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in file get: {e}")


class TestFileStoreAsync:
    """Test asynchronous file store operations"""
    
    uploaded_keys = []  # Track uploaded files for cleanup
    
    @pytest.mark.parametrize("test_case", TEST_CASES_UPLOAD, ids=[tc["name"] for tc in TEST_CASES_UPLOAD])
    @pytest.mark.asyncio
    async def test_file_upload_async(self, test_case):
        """Test asynchronous file upload with various options"""
        try:
            result = await async_jigsaw.store.upload(test_case["file"], test_case["options"])
            
            print(f"Async upload test {test_case['name']}: {result}")
            assert result.get("key") is not None
            assert result.get("url") is not None
            assert result.get("size") > 0
            
            # Check temp_public_url if requested
            if test_case.get("options") and test_case["options"].get("temp_public_url"):
                assert result.get("temp_public_url") is not None
            
            # Store key for cleanup
            self.uploaded_keys.append(result["key"])
            
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in async {test_case['name']}: {e}")
    
    @pytest.mark.asyncio
    async def test_file_get_async(self):
        """Test asynchronous file retrieval"""
        # First upload a file to retrieve
        test_key = f"test-async-get-{uuid.uuid4().hex[:8]}.txt"
        try:
            upload_result = await async_jigsaw.store.upload(
                TEXT_FILE_CONTENT,
                {"key": test_key, "content_type": "text/plain"}
            )
            
            # Now retrieve it
            file_content = await async_jigsaw.store.get(upload_result["key"])
            assert file_content is not None
            print(f"Async retrieved file with key {upload_result['key']}")
            
            # Cleanup
            self.uploaded_keys.append(upload_result["key"])
            
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in async file get: {e}")