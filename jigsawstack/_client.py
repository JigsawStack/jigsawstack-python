from typing import Union
import os
from .audio import Audio
from .vision import Vision
from .searchs import Search
from .predictions import Prediction
from .sql import SQL
from .store import KV, File
from .translate import Translate
from .web import Web
from .sentiment import Sentiment
from .validate import Validate
from .summary import Summary

class JigsawStack:
    audio: Audio
    vision : Vision
    prediction: Prediction
    sql: SQL
    file: File
    kv: KV
    translate: Translate
    web: Web
    sentiment: Sentiment
    validate: Validate
    summary: Summary
    search: Search
    api_key: str
    api_url: str


    def __init__(self, api_key: Union[str, None] = None, api_url: Union[str, None] = None) -> None:
        if api_key is None:
            api_key = os.environ.get("JIGSAWSTACK_API_KEY")
        
        if api_key is None:
            raise ValueError("The api_key client option must be set either by passing api_key to the client or by setting the JIGSAWSTACK_API_KEY environment variable")
        
        if api_url is None:
            api_url = os.environ.get("JIGSAWSTACK_API_URL")
        if api_url is None:
            api_url = f"https://api.jigsawstack.com/v1"

        self.api_key = api_key
        self.api_url = api_url


        self.audio = Audio(api_key=api_key, api_url=api_url)
        self.web = Web(api_key=api_key, api_url=api_url)
        self.search = Search(api_key=api_key, api_url=api_url)
        self.sentiment = Sentiment(api_key=api_key, api_url=api_url)
        self.validate = Validate(api_key=api_key, api_url=api_url)
        self.summary = Summary(api_key=api_key, api_url=api_url)
        self.vision = Vision(api_key=api_key, api_url=api_url)
        self.prediction = Prediction(api_key=api_key, api_url=api_url)
        self.sql = SQL(api_key=api_key, api_url=api_url)
        self.file = File(api_key=api_key, api_url=api_url)
        self.kv = KV(api_key=api_key, api_url=api_url)
        self.translate = Translate(api_key=api_key, api_url=api_url)
