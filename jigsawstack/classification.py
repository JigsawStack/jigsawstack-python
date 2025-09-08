from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict, Literal
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig
from ._types import BaseResponse


class DatasetItem(TypedDict):
    type: Literal["text", "image"]
    """
    Type of the dataset item: text
    """

    value: str
    """
    Value of the dataset item
    """


class LabelItem(TypedDict):
    key: NotRequired[str]
    """
    Optional key for the label
    """

    type: Literal["text", "image"]
    """
    Type of the label: text
    """

    value: str
    """
    Value of the label
    """


class ClassificationParams(TypedDict):
    dataset: List[DatasetItem]
    """
    List of text dataset items to classify
    """

    labels: List[LabelItem]
    """
    List of text labels for classification
    """

    multiple_labels: NotRequired[bool]
    """
    Whether to allow multiple labels per item
    """


class ClassificationResponse(BaseResponse):
    predictions: List[Union[str, List[str]]]
    """
    Classification predictions - single labels or multiple labels per item
    """


class Classification(ClientConfig):
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

    def classify(self, params: ClassificationParams) -> ClassificationResponse:
        path = "/classification"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp


class AsyncClassification(ClientConfig):
    config: AsyncRequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        disable_request_logging: Union[bool, None] = False,
    ):
        super().__init__(api_key, api_url, disable_request_logging)
        self.config = AsyncRequestConfig(
            api_url=api_url,
            api_key=api_key,
            disable_request_logging=disable_request_logging,
        )

    async def classify(self, params: ClassificationParams) -> ClassificationResponse:
        path = "/classification"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
