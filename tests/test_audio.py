from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.translate
import jigsawstack.translate._translate
import jigsawstack.audio
import jigsawstack

# flake8: noqa

class TestAudioAPI(unittest.TestCase):

    def test_speech_to_text_success_response(self) -> None:
        params = {
           "url":"https://rogilvkqloanxtvjfrkm.supabase.co/storage/v1/object/public/demo/Video%201737458382653833217.mp4?t=2024-03-22T09%3A50%3A49.894Z"
        }
        try:
            result = jigsawstack.Audio.speech_to_text(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."