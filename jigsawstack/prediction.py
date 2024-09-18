from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from typing import List, Union
from ._config import ClientConfig


class Dataset(TypedDict):
    value: int
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
    The number of predictions to make. The defualt is 5. 
    """


class PredictionResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    prediction: object


class Prediction(ClientConfig):

    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
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
