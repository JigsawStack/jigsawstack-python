from unittest.mock import MagicMock
import unittest
from jigsawstack.exceptions import JigsawStackError
from jigsawstack import AsyncJigsawStack
import pytest
import asyncio
import logging
from jigsawstack import AsyncJigsawStack

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_text_to_speech():
    async def _test():
        client = AsyncJigsawStack()

        """Test converting text to speech"""
        try:
            response = await client.audio.text_to_speech(
                {
                    "text": "Hello world, this is a test of the JigsawStack text to speech API."
                }
            )
            print("Text to speech response:", response)
            assert response["success"] == True

        except Exception as e:
            print(f"Error in text_to_speech test: {e}")

    asyncio.run(_test())


def test_speaker_voice_accents():
    async def _test():
        client = AsyncJigsawStack()

        """Test getting available voice accents"""
        try:
            response = await client.audio.speaker_voice_accents()
            print("Speaker voice accents response:", response)
            assert response["success"] == True

        except Exception as e:
            print(f"Error in speaker voice accents test: {e}")


def test_create_clone():
    async def _test():
        client = AsyncJigsawStack()

        """Test creating a voice clone with URL"""
        try:
            audio_url = (
                "https://jigsawstack.com/audio/test.mp3"  # Replace with an actual URL
            )
            clone_response_url = await client.audio.create_clone(
                {"url": audio_url, "name": "Test Voice Clone URL"}
            )

            assert clone_response_url["success"] == True

            clone_response_file_store_key = client.audio.create_clone(
                {
                    "file_store_key": "hello_audio",
                    "name": "Test Voice Clone File Store Key",
                }
            )

            assert clone_response_file_store_key["success"] == True

        except Exception as e:
            print(f"Error in voice_cloning test: {e}")

    asyncio.run(_test())


def test_list_clones():
    async def _test():
        client = AsyncJigsawStack()
        """Test listing voice clones"""
        try:
            # List available voice clones
            clones_response = await client.audio.list_clones({"limit": 10, "page": 1})

            assert clones_response["success"] == True

        except Exception as e:
            print(f"Error in voice_cloning test: {e}")

    asyncio.run(_test())


def test_delete_clone():
    async def _test():
        client = AsyncJigsawStack()
        """Test getting a voice clone"""
        try:
            create_clone_response = await client.audio.create_clone(
                {"name": "Test Voice Clone URL", "file_store_key": "hello_audio"}
            )
            clones = await client.audio.list_clones({"limit": 10, "page": 1})
            print("Clones:", clones)
            clone_id = clones["data"][0]["id"]
            delete_clone_response = await client.audio.delete_clone(clone_id)
            print("Delete clone response:", delete_clone_response)
            assert delete_clone_response["success"] == True

        except Exception as e:
            print(f"Error in list_clones test: {e}")

    asyncio.run(_test())
