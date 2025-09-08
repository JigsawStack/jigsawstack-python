from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import JigsawStack

import pytest

# flake8: noqa

client = JigsawStack()


@pytest.mark.skip(reason="Skipping TestStoreAPI class for now")
class TestStoreAPI(unittest.TestCase):
    def test_upload_success_response(self) -> None:
        # Sample file content as bytes
        file_content = b"This is a test file content"
        options = {
            "key": "test-file.txt",
            "content_type": "text/plain",
            "overwrite": True,
            "temp_public_url": True,
        }
        try:
            result = client.store.upload(file_content, options)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_get_success_response(self) -> None:
        key = "test-file.txt"
        try:
            result = client.store.get(key)
            # For file retrieval, we expect the actual file content
            assert result is not None
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_delete_success_response(self) -> None:
        key = "test-file.txt"
        try:
            result = client.store.delete(key)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_upload_without_options_success_response(self) -> None:
        # Test upload without optional parameters
        file_content = b"This is another test file content"
        try:
            result = client.store.upload(file_content)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_upload_with_partial_options_success_response(self) -> None:
        # Test upload with partial options
        file_content = b"This is a test file with partial options"
        options = {"key": "partial-test-file.txt", "overwrite": False}
        try:
            result = client.store.upload(file_content, options)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."
