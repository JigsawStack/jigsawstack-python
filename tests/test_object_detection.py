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

IMAGE_URL = "https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Collabo%201080x842.jpg"

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
        "name": "annotated_image_true",
        "blob": IMAGE_URL,
        "options": {"annotated_image": True},
    },
    {
        "name": "with_annotated_image_false",
        "blob": IMAGE_URL,
        "options": {"annotated_image": False},
    },
    {
        "name": "with_blob_both_features",
        "blob": IMAGE_URL,
        "options": {
            "features": ["object", "gui"],
            "annotated_image": True,
            "return_type": "url",
        },
    },
    {
        "name": "with_blob_gui_features",
        "blob": IMAGE_URL,
        "options": {"features": ["gui"], "annotated_image": False},
    },
    {
        "name": "with_blob_object_detection_features",
        "blob": IMAGE_URL,
        "options": {
            "features": ["object"],
            "annotated_image": True,
            "return_type": "base64",
        },
    },
    {
        "name": "with_prompts",
        "blob": IMAGE_URL,
        "options": {
            "prompts": ["castle", "tree"],
            "annotated_image": True,
        },
    },
    {
        "name": "with_all_options",
        "blob": IMAGE_URL,
        "options": {
            "features": ["object", "gui"],
            "prompts": ["car", "road", "tree"],
            "annotated_image": True,
            "return_type": "base64",
            "return_masks": False,
        },
    },
]


class TestObjectDetectionSync:
    """Test synchronous object detection methods"""

    sync_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_object_detection(self, test_case):
        """Test synchronous object detection with various inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = jigsaw.vision.object_detection(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = jigsaw.vision.object_detection(test_case["params"])

            print(f"Test {test_case['name']}: {result}")
            assert result["success"]
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestObjectDetectionAsync:
    """Test asynchronous object detection methods"""

    async_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_object_detection_async(self, test_case):
        """Test asynchronous object detection with various inputs"""
        try:
            if test_case.get("blob"):
                # Download blob content
                blob_content = requests.get(test_case["blob"]).content
                result = await async_jigsaw.vision.object_detection(
                    blob_content, test_case.get("options", {})
                )
            else:
                # Use params directly
                result = await async_jigsaw.vision.object_detection(test_case["params"])

            print(f"Test {test_case['name']}: {result}")
            assert result["success"]
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
