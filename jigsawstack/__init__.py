from typing import Union
import os
from .audio import Audio
from .vision import Vision
from .search import Search
from .prediction import Prediction
from .sql import SQL
from .store import KV, Store
from .translate import Translate
from .web import Web
from .sentiment import Sentiment
from .validate import Validate
from .summary import Summary
from .geo import Geo
from .prompt_engine import PromptEngine
from .exceptions import JigsawStackError

# from .version import get_version


class JigsawStack:
    audio: Audio
    vision: Vision
    prediction: Prediction
    text_to_sql: SQL
    file: Store
    kv: KV
    translate: Translate
    web: Web
    sentiment: Sentiment
    validate: Validate
    summary: Summary
    search: Search
    geo: Geo
    prompt_engine: PromptEngine
    api_key: str
    api_url: str
    disable_request_logging: bool

    def __init__(
        self,
        api_key: Union[str, None] = None,
        api_url: Union[str, None] = None,
        disable_request_logging: Union[bool, None] = None,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("JIGSAWSTACK_API_KEY")

        if api_key is None:
            raise ValueError(
                "The api_key client option must be set either by passing api_key to the client or by setting the JIGSAWSTACK_API_KEY environment variable"
            )

        if api_url is None:
            api_url = os.environ.get("JIGSAWSTACK_API_URL")
        if api_url is None:
            api_url = f"https://api.jigsawstack.com/v1"

        self.api_key = api_key
        self.api_url = api_url

        self.audio = Audio(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.web = Web(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.sentiment = Sentiment(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).analyze
        self.validate = Validate(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.summary = Summary(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).summarize
        self.vision = Vision(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.prediction = Prediction(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).predict
        self.text_to_sql = SQL(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).text_to_sql
        self.store = Store(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.kv = KV(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.translate = Translate(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).translate
        self.geo = Geo(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.prompt_engine = PromptEngine(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )


# Create a global instance of the Web class
__all__ = ["JigsawStack", "Search", "JigsawStackError"]
