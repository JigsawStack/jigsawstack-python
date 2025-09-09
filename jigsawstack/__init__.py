from typing import Union, Dict
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
from .embedding import Embedding, AsyncEmbedding
from .exceptions import JigsawStackError
from .image_generation import ImageGeneration, AsyncImageGeneration
from .classification import Classification, AsyncClassification
from .prompt_engine import PromptEngine, AsyncPromptEngine
from .embeddingV2 import EmbeddingV2, AsyncEmbeddingV2


class JigsawStack:
    audio: Audio
    vision: Vision
    image_generation: ImageGeneration
    file: Store
    web: Web
    search: Search
    classification: Classification
    prompt_engine: PromptEngine
    api_key: str
    api_url: str
    headers: Dict[str, str]
    # disable_request_logging: bool

    def __init__(
        self,
        api_key: Union[str, None] = None,
        api_url: Union[str, None] = None,
        # disable_request_logging: Union[bool, None] = None,
        headers: Union[Dict[str, str], None] = None,
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
            api_url = f"https://api.jigsawstack.com/"

        self.api_key = api_key
        self.api_url = api_url

        self.headers = headers or {}

        disable_request_logging = self.headers.get("x-jigsaw-no-request-log")

        self.audio = Audio(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )
        self.web = Web(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )
        self.sentiment = Sentiment(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).analyze
        self.validate = Validate(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )
        self.summary = Summary(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).summarize
        self.vision = Vision(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )
        self.prediction = Prediction(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).predict
        self.text_to_sql = SQL(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).text_to_sql
        self.store = Store(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )
        self.translate = Translate(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )

        self.embedding = Embedding(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).execute

        self.embeddingV2 = EmbeddingV2(
            api_key=api_key,
            api_url=api_url + "/v2",
            disable_request_logging=disable_request_logging,
        ).execute

        self.image_generation = ImageGeneration(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).image_generation

        self.classification = Classification(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).classify

        self.prompt_engine = PromptEngine(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )


class AsyncJigsawStack:
    validate: AsyncValidate
    web: AsyncWeb
    audio: AsyncAudio
    vision: AsyncVision
    image_generation: AsyncImageGeneration
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
            api_url = f"https://api.jigsawstack.com/"

        self.api_key = api_key
        self.api_url = api_url

        self.web = AsyncWeb(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )

        self.validate = AsyncValidate(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )
        self.audio = AsyncAudio(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )

        self.vision = AsyncVision(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )

        self.store = AsyncStore(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )

        self.summary = AsyncSummary(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).summarize

        self.prediction = AsyncPrediction(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).predict
        self.text_to_sql = AsyncSQL(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).text_to_sql

        self.sentiment = AsyncSentiment(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).analyze

        self.translate = AsyncTranslate(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )

        self.embedding = AsyncEmbedding(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).execute

        self.embeddingV2 = AsyncEmbeddingV2(
            api_key=api_key,
            api_url=api_url + "/v2",
            disable_request_logging=disable_request_logging,
        ).execute

        self.image_generation = AsyncImageGeneration(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).image_generation

        self.classification = AsyncClassification(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        ).classify

        self.prompt_engine = AsyncPromptEngine(
            api_key=api_key,
            api_url=api_url + "/v1",
            disable_request_logging=disable_request_logging,
        )


# Create a global instance of the Web class
__all__ = ["JigsawStack", "Search", "JigsawStackError", "AsyncJigsawStack"]
