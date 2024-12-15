from typing import Union
import os
from .audio import Audio, AsyncAudio
from .vision import Vision, AsyncVision
from .search import Search
from .prediction import Prediction, AsyncPrediction
from .sql import SQL, AsyncSQL
from .store import Store, AsyncStore
from .translate import Translate, AsyncTranslate
from .web import Web, AsyncWeb
from .sentiment import Sentiment, AsyncSentiment
from .validate import Validate, AsyncValidate
from .summary import Summary, AsyncSummary
from .geo import Geo, AsyncGeo
from .prompt_engine import PromptEngine, AsyncPromptEngine
from .exceptions import JigsawStackError


class JigsawStack:
    audio: Audio
    vision: Vision
    file: Store
    web: Web
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


class AsyncJigsawStack:
    geo: AsyncGeo
    validate: AsyncValidate
    web: AsyncWeb
    audio: AsyncAudio
    vision: AsyncVision
    store: AsyncStore
    prompt_engine: AsyncPromptEngine
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

        self.web = AsyncWeb(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )

        self.geo = AsyncGeo(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )

        self.validate = AsyncValidate(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )
        self.audio = AsyncAudio(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )

        self.vision = AsyncVision(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )

        self.store = AsyncStore(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )

        self.summary = AsyncSummary(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).summarize

        self.prediction = AsyncPrediction(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).predict
        self.text_to_sql = AsyncSQL(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).text_to_sql

        self.sentiment = AsyncSentiment(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).analyze

        self.translate = AsyncTranslate(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        ).translate

        self.prompt_engine = AsyncPromptEngine(
            api_key=api_key,
            api_url=api_url,
            disable_request_logging=disable_request_logging,
        )


# Create a global instance of the Web class
__all__ = ["JigsawStack", "Search", "JigsawStackError", "AsyncJigsawStack"]
