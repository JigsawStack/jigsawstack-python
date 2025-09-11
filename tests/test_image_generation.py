import requests
from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest
import logging
from dotenv import load_dotenv
import os
import base64

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))

IMAGE_URL = "https://images.unsplash.com/photo-1494588024300-e9df7ff98d78?q=80&w=1284&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
FILE_STORE_KEY = jigsaw.store.upload(requests.get(IMAGE_URL).content, {
                "filename": "test_image.jpg",
                "content_type": "image/jpeg",
                "overwrite": True
            })

TEST_CASES = [
    {
        "name": "basic_generation_with_prompt",
        "params": {
            "prompt": "A beautiful mountain landscape at sunset",
        },
    },
    {
        "name": "with_aspect_ratio",
        "params": {
            "prompt": "A serene lake with mountains in the background",
            "aspect_ratio": "16:9"
        },
    },
    {
        "name": "with_custom_dimensions",
        "params": {
            "prompt": "A futuristic city skyline",
            "width": 1024,
            "height": 768
        },
    },
    {
        "name": "with_output_format_png",
        "params": {
            "prompt": "A colorful abstract painting",
            "output_format": "png"
        },
    },
    {
        "name": "with_advanced_config",
        "params": {
            "prompt": "A realistic portrait of a person",
            "advance_config": {
                "negative_prompt": "blurry, low quality, distorted",
                "guidance": 7,
                "seed": 42
            }
        },
    },
    {
        "name": "with_steps",
        "params": {
            "prompt": "A detailed botanical illustration",
            "steps": 30,
            "aspect_ratio": "3:4",
            "return_type": "base64"
        },
    },
    {
        "name": "with_return_type_url",
        "params": {
            "prompt": "A vintage car on a desert road",
            "return_type": "url"
        },
    },
    {
        "name": "with_return_type_base64",
        "params": {
            "prompt": "A fantasy castle on a hill",
            "return_type": "base64"
        }
    },
    {
        "name": "with_all_options",
        "params": {
            "prompt": "An intricate steampunk clockwork mechanism",
            "aspect_ratio": "4:3",
            "steps": 25,
            "output_format": "png",
            "advance_config": {
                "negative_prompt": "simple, plain, boring",
                "guidance": 8,
                "seed": 12345
            },
            "return_type": "base64"
        },
    },
]

# Test cases for image-to-image generation (using existing images as input)
IMAGE_TO_IMAGE_TEST_CASES = [
    {
        "name": "with_url",
        "params": {
            "prompt": "Add snow effects to this image",
            "url": IMAGE_URL,
            "return_type": "base64"
        },
    },
    {
        "name": "with_file_store_key",
        "params": {
            "prompt": "Apply a cyberpunk style to this image",
            "file_store_key": FILE_STORE_KEY,
        },
    }
]


class TestImageGenerationSync:
    """Test synchronous image generation methods"""
    
    @pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc["name"] for tc in TEST_CASES])
    def test_image_generation(self, test_case):
        """Test synchronous image generation with various parameters"""
        try:
            result = jigsaw.image_generation(test_case["params"])

            print(type(result))

            if isinstance(result, dict):
                print(result)
            # Check response structure
            assert result is not None

            if type(result) is dict:

                # Check for image data based on return_type
                if test_case["params"].get("return_type") == "url":
                    assert result.get("url") is not None
                    assert requests.get(result["url"]).status_code == 200
                    assert isinstance(result["url"], str)
                elif test_case["params"].get("return_type") == "base64":
                    assert result.get("url") is not None
                elif test_case["params"].get("return_type") == "url":
                    assert result.get("url") is not None
                    assert requests.get(result["url"]).status_code == 200
            else:
                assert isinstance(result, bytes)
            
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
    
    @pytest.mark.parametrize("test_case", IMAGE_TO_IMAGE_TEST_CASES[:1], ids=[tc["name"] for tc in IMAGE_TO_IMAGE_TEST_CASES[:1]])
    def test_image_to_image_generation(self, test_case):
        """Test image-to-image generation with URL input"""
        try:
            
            result = jigsaw.image_generation(test_case["params"])
            
            print(f"Test {test_case['name']}: Generated image from input")
            assert result is not None
            
            if type(result) is dict:
                assert result.get("success") == True
                assert result.get("url") is not None
            elif type(result) is bytes:
                assert isinstance(result, bytes)
            else:
                pytest.fail(f"Unexpected result type in {test_case['name']}: {type(result)}")
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestImageGenerationAsync:
    """Test asynchronous image generation methods"""
    
    @pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc["name"] for tc in TEST_CASES])
    @pytest.mark.asyncio
    async def test_image_generation_async(self, test_case):
        """Test asynchronous image generation with various parameters"""
        try:
            result = await async_jigsaw.image_generation(test_case["params"])
            
            print(f"Async test {test_case['name']}: Generated image")
            
            # Check response structure
            assert result is not None
            if type(result) is dict:
            # Check for image data based on return_type
                if test_case["params"].get("return_type") == "url":
                    assert result.get("url") is not None
                    assert requests.get(result["url"]).status_code == 200
                    assert isinstance(result["url"], str)
                    assert result["url"].startswith("http")
                elif test_case["params"].get("return_type") == "base64":
                    assert result.get("url") is not None
                elif test_case["params"].get("return_type") == "url":
                    assert result.get("url") is not None
                    assert requests.get(result["url"]).status_code == 200
            else:
                assert isinstance(result, bytes)
            
        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in async {test_case['name']}: {e}")
    
    @pytest.mark.parametrize("test_case", IMAGE_TO_IMAGE_TEST_CASES[:1], ids=[tc["name"] for tc in IMAGE_TO_IMAGE_TEST_CASES[:1]])
    @pytest.mark.asyncio
    async def test_image_to_image_generation_async(self, test_case):
        """Test asynchronous image-to-image generation with URL input"""
        try:
            result = await async_jigsaw.image_generation(test_case["params"])

            assert result is not None
            if type(result) is dict:
                assert result.get("success") == True
                assert result.get("url") is not None
            elif type(result) is bytes:
                assert isinstance(result, bytes)
            else:
                pytest.fail(f"Unexpected result type in {test_case['name']}: {type(result)}")

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in async {test_case['name']}: {e}")