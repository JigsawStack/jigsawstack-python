import os
from typing import Dict, Union

from .audio import AsyncAudio, Audio
from .classification import AsyncClassification, Classification
from .embedding import AsyncEmbedding, Embedding
from .embedding_v2 import AsyncEmbeddingV2, EmbeddingV2
from .exceptions import JigsawStackError
from .image_generation import AsyncImageGeneration, ImageGeneration
from .prediction import AsyncPrediction, Prediction
from .prompt_engine import AsyncPromptEngine, PromptEngine
from .search import Search
from .sentiment import AsyncSentiment, Sentiment
from .sql import SQL, AsyncSQL
from .store import AsyncStore, Store
from .summary import AsyncSummary, Summary
from .translate import AsyncTranslate, Translate
from .validate import AsyncValidate, Validate
from .vision import AsyncVision, Vision
from .web import AsyncWeb, Web


class JigsawStack:
    api_key: str
    api_url: str
    headers: Dict[str, str]
    audio: Audio
    classification: Classification
    embedding: Embedding
    embedding_v2: EmbeddingV2
    store: Store
    image_generation: ImageGeneration
    prediction: Prediction
    prompt_engine: PromptEngine
    sentiment: Sentiment
    summary: Summary
    text_to_sql: SQL
    translate: Translate
    validate: Validate
    vision: Vision
    web: Web

    def __init__(
        self,
        api_key: Union[str, None] = None,
        api_url: Union[str, None] = None,
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
            api_url = "https://api.jigsawstack.com/"

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

        self.embedding_v2 = EmbeddingV2(
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
    api_key: str
    api_url: str
    headers: Dict[str, str]
    audio: AsyncAudio
    classification: AsyncClassification
    embedding: AsyncEmbedding
    embedding_v2: AsyncEmbeddingV2
    image_generation: AsyncImageGeneration
    prediction: AsyncPrediction
    prompt_engine: AsyncPromptEngine
    sentiment: AsyncSentiment
    store: AsyncStore
    summary: AsyncSummary
    text_to_sql: AsyncSQL
    translate: AsyncTranslate
    validate: AsyncValidate
    vision: AsyncVision
    web: AsyncWeb

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
            api_url = "https://api.jigsawstack.com/"

        self.api_key = api_key
        self.api_url = api_url
        disable_request_logging = self.headers.get("x-jigsaw-no-request-log")

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

        self.embedding_v2 = AsyncEmbeddingV2(
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
