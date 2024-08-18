
from . import resources
from typing import Union
from ._config import ClientConfig
import os


class JigsawStack:
    audio: resources.Audio
    vision : resources.Vision
    prediction: resources.Prediction
    sql: resources.SQL
    file: resources.File
    kv: resources.KV
    translate: resources.Translate
    web: resources.Web
    sentiment: resources.Sentiment
    validate: resources.Validate
    summary: resources.Summary
    search: resources.Search
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


        self.audio = resources.Audio(api_key=api_key, api_url=api_url)
        self.web = resources.Web(api_key=api_key, api_url=api_url)
        self.search = resources.Search(api_key=api_key, api_url=api_url)
        self.sentiment = resources.Sentiment(api_key=api_key, api_url=api_url)
        self.validate = resources.Validate(api_key=api_key, api_url=api_url)
        self.summary = resources.Summary(api_key=api_key, api_url=api_url)
        self.vision = resources.Vision(api_key=api_key, api_url=api_url)
        self.prediction = resources.Prediction(api_key=api_key, api_url=api_url)
        self.sql = resources.SQL(api_key=api_key, api_url=api_url)
        self.file = resources.File(api_key=api_key, api_url=api_url)
        self.kv = resources.KV(api_key=api_key, api_url=api_url)
        self.translate = resources.Translate(api_key=api_key, api_url=api_url)
