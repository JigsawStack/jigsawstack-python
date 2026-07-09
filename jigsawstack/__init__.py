import os
from typing import Dict, List, Optional, Union

import aiohttp

from ._config import ClientConfig
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
    base_url: str
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
        base_url: Union[str, None] = None,
        headers: Union[Dict[str, str], None] = None,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("JIGSAWSTACK_API_KEY")

        if api_key is None:
            raise ValueError(
                "The api_key client option must be set either by passing api_key to the client or by setting the JIGSAWSTACK_API_KEY environment variable"
            )

        if base_url is None:
            base_url = os.environ.get("JIGSAWSTACK_API_URL")
        if base_url is None:
            base_url = "https://api.jigsawstack.com/"

        self.api_key = api_key
        self.base_url = base_url

        self.headers = headers or {"Content-Type": "application/json"}

        self.audio = Audio(api_key=api_key, base_url=base_url + "/v1", headers=headers)

        self.web = Web(api_key=api_key, base_url=base_url + "/v1", headers=headers)

        self.sentiment = Sentiment(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        ).analyze

        self.validate = Validate(api_key=api_key, base_url=base_url + "/v1", headers=headers)
        self.summary = Summary(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        ).summarize

        self.vision = Vision(api_key=api_key, base_url=base_url + "/v1", headers=headers)

        self.prediction = Prediction(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        ).predict

        self.text_to_sql = SQL(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        ).text_to_sql

        self.store = Store(api_key=api_key, base_url=base_url + "/v1", headers=headers)

        self.translate = Translate(api_key=api_key, base_url=base_url + "/v1", headers=headers)

        self.embedding = Embedding(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        ).execute

        self.embedding_v2 = EmbeddingV2(
            api_key=api_key, base_url=base_url + "/v2", headers=headers
        ).execute

        self.image_generation = ImageGeneration(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        ).image_generation

        self.classification = Classification(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        ).classify

        self.prompt_engine = PromptEngine(
            api_key=api_key, base_url=base_url + "/v1", headers=headers
        )


class AsyncJigsawStack:
    api_key: str
    base_url: str
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
        base_url: Union[str, None] = None,
        headers: Union[Dict[str, str], None] = None,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("JIGSAWSTACK_API_KEY")

        if api_key is None:
            raise ValueError(
                "The api_key client option must be set either by passing api_key to the client or by setting the JIGSAWSTACK_API_KEY environment variable"
            )

        if base_url is None:
            base_url = os.environ.get("JIGSAWSTACK_API_URL")
        if base_url is None:
            base_url = "https://api.jigsawstack.com/"

        self.api_key = api_key
        self.base_url = base_url
        self.headers = headers or {"Content-Type": "application/json"}

        # _async_services holds every async service instance so that
        # __aenter__ / aclose() can inject / remove the shared session.
        self._async_services: List[ClientConfig] = []
        self._session: Optional[aiohttp.ClientSession] = None

        def _reg(svc: ClientConfig) -> ClientConfig:
            self._async_services.append(svc)
            return svc

        self.web = _reg(AsyncWeb(api_key=api_key, base_url=base_url + "/v1", headers=headers))

        self.validate = _reg(AsyncValidate(api_key=api_key, base_url=base_url + "/v1", headers=headers))

        self.audio = _reg(AsyncAudio(api_key=api_key, base_url=base_url + "/v1", headers=headers))

        self.vision = _reg(AsyncVision(api_key=api_key, base_url=base_url + "/v1", headers=headers))

        self.store = _reg(AsyncStore(api_key=api_key, base_url=base_url + "/v1", headers=headers))

        _summary = _reg(AsyncSummary(api_key=api_key, base_url=base_url + "/v1", headers=headers))
        self.summary = _summary.summarize

        _prediction = _reg(AsyncPrediction(api_key=api_key, base_url=base_url + "/v1", headers=headers))
        self.prediction = _prediction.predict

        _sql = _reg(AsyncSQL(api_key=api_key, base_url=base_url + "/v1", headers=headers))
        self.text_to_sql = _sql.text_to_sql

        _sentiment = _reg(AsyncSentiment(api_key=api_key, base_url=base_url + "/v1", headers=headers))
        self.sentiment = _sentiment.analyze

        self.translate = _reg(AsyncTranslate(api_key=api_key, base_url=base_url + "/v1", headers=headers))

        _embedding = _reg(AsyncEmbedding(api_key=api_key, base_url=base_url + "/v1", headers=headers))
        self.embedding = _embedding.execute

        _embedding_v2 = _reg(AsyncEmbeddingV2(api_key=api_key, base_url=base_url + "/v2", headers=headers))
        self.embedding_v2 = _embedding_v2.execute

        _image_gen = _reg(AsyncImageGeneration(api_key=api_key, base_url=base_url + "/v1", headers=headers))
        self.image_generation = _image_gen.image_generation

        _classification = _reg(AsyncClassification(api_key=api_key, base_url=base_url + "/v1", headers=headers))
        self.classification = _classification.classify

        self.prompt_engine = _reg(AsyncPromptEngine(api_key=api_key, base_url=base_url + "/v1", headers=headers))

    async def __aenter__(self) -> "AsyncJigsawStack":
        """Open a shared aiohttp.ClientSession reused across all requests."""
        self._session = aiohttp.ClientSession()
        for svc in self._async_services:
            svc.config["session"] = self._session
        return self

    async def aclose(self) -> None:
        """Close the shared session and clear it from all service configs."""
        if self._session is not None:
            for svc in self._async_services:
                svc.config.pop("session", None)
            await self._session.close()
            self._session = None

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        await self.aclose()


# Create a global instance of the Web class
__all__ = ["JigsawStack", "Search", "JigsawStackError", "AsyncJigsawStack"]
