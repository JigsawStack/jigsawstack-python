from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from jigsawstack import request
from typing import List, Union

class Dataset(TypedDict):
    value : int
    """
    The value of the dataset.
    """

    date : str
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



class Prediction:
    @classmethod
    def predict(cls, params: PredictionParams) -> PredictionResponse:
        path = "/ai/prediction"
        resp = request.Request(path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
        return resp


