from typing import Any, Dict, List, Union, cast

from typing_extensions import TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest
from .request import Request, RequestConfig


class Dataset(TypedDict):
    value: Union[int, float, str]
    """
    The value of the dataset.
    """

    date: str
    """
    The date of the dataset.
    """


class PredictionParams(TypedDict):
    dataset: List[Dataset]
    """
    The dataset to make predictions on. This is an array of object with keys date and value. See example below for more information.
    """
    steps: int
    """
    The number of predictions to make. The default is 5.
    """


class PredictionResponse(BaseResponse):
    steps: int
    """
    The number of steps predicted.
    """
    prediction: List[Dataset]
    """
    The predictions made on the dataset.
    """


class Prediction(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    def predict(self, params: PredictionParams) -> PredictionResponse:
        path = "/ai/prediction"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp


class AsyncPrediction(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
        )

    async def predict(self, params: PredictionParams) -> PredictionResponse:
        path = "/ai/prediction"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
