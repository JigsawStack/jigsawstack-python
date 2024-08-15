import os
from .web.web import Web
from .audio.audio import Audio
from .validate.validate import Validate
from .vision.vision import Vision
from .vision.vision import Vision
from .store.kv import KV
from .store.file import File

# Config vars
api_key = os.environ.get("JIGSAWSTACK_API_KEY")
api_url = os.environ.get("JIGSAWSTACK_API_URL", "https://api.jigsawstack.com")



# Create a global instance of the Web class
__all__ = ["Web", "Audio", "Validate", "Vision", "KV", "File"]