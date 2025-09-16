from typing import Any, Dict, List, Union, cast

from typing_extensions import Literal, NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest, AsyncRequestConfig
from .request import Request, RequestConfig


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
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = RequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
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
        base_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, base_url, headers)
        self.config = AsyncRequestConfig(
            base_url=base_url,
            api_key=api_key,
            headers=headers,
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
