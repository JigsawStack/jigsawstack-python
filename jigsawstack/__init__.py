import os
from .web.web import Web
from .audio.audio import Audio
from .validate.validate import Validate
from .vision.vision import Vision
from .vision.vision import Vision
from .store.kv import KV
from .store.file import File
from .translate._translate import Translate
from .prediction._prediction import Prediction
from .search._search import Search
from .summary._summary import Summary
from .sentiment._sentiment import Sentiment
from .sql._sql import SQL

# Config vars
api_key = os.environ.get("JIGSAWSTACK_API_KEY", "")
api_url = os.environ.get("JIGSAWSTACK_API_URL", "https://api.jigsawstack.com")


# Create a global instance of the Web class
__all__ = ["Web", "Audio", "Validate", "Vision", "KV", "File","Translate", "Prediction", "Search","Summary", "Sentiment","SQL"]