import os
from ._client import JigsawStack

# Config vars
api_key = os.environ.get("JIGSAWSTACK_API_KEY", "")
api_url = os.environ.get("JIGSAWSTACK_API_URL", "https://api.jigsawstack.com")


# Create a global instance of the Web class
__all__ = ["JigsawStack"]