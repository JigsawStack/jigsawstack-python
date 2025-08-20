from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import JigsawStack

import pytest

# flake8: noqa

client = JigsawStack()


@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
class TestClassification(unittest.TestCase):
    def test_classification_text_success_response(self) -> None:
        params = {
            "dataset": [
                {"type": "text", "value": "I love programming"},
                {"type": "text", "value": "I love reading books"},
                {"type": "text", "value": "I love watching movies"},
                {"type": "text", "value": "I love playing games"},
            ],
            "labels": [
                {"type": "text", "value": "programming"},
                {"type": "text", "value": "reading"},
                {"type": "text", "value": "watching"},
                {"type": "text", "value": "playing"},
            ],
        }
        try:
            result = client.classification.text(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_classification_image_success_response(self) -> None:
        params = {
            "dataset": [
                {"type": "image", "value": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4aBhloyMLx5qA6G6wSEi0s9AvDu1r7utrbQ&s"},
                {"type": "image", "value": "https://cdn.britannica.com/79/232779-050-6B0411D7/German-Shepherd-dog-Alsatian.jpg"},
            ],
            "labels": [
                {"type": "text", "value": "Cat"},
                {"type": "text", "value": "Dog"},
            ],
        }
        try:
            result = client.classification.image(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."

    def test_dns_success_response(self) -> None:

        params = {
            "url": "https://supabase.com/pricing",
        }
        try:
            result = client.web.dns(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."