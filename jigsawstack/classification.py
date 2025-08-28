from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict, Literal
from .request import Request, RequestConfig
from .async_request import AsyncRequest, AsyncRequestConfig
from ._config import ClientConfig


class DatasetItemText(TypedDict):
    type: Literal["text"]
    """
    Type of the dataset item: text
    """

    value: str
    """
    Value of the dataset item
    """


class DatasetItemImage(TypedDict):
    type: Literal["image"]
    """
    Type of the dataset item: image
    """

    value: str
    """
    Value of the dataset item
    """


class LabelItemText(TypedDict):
    key: NotRequired[str]
    """
    Optional key for the label
    """

    type: Literal["text"]
    """
    Type of the label: text
    """

    value: str
    """
    Value of the label
    """


class LabelItemImage(TypedDict):
    key: NotRequired[str]
    """
    Optional key for the label
    """

    type: Literal["image", "text"]
    """
    Type of the label: image or text
    """

    value: str
    """
    Value of the label
    """


class ClassificationTextParams(TypedDict):
    dataset: List[DatasetItemText]
    """
    List of text dataset items to classify
    """

    labels: List[LabelItemText]
    """
    List of text labels for classification
    """

    multiple_labels: NotRequired[bool]
    """
    Whether to allow multiple labels per item
    """


class ClassificationImageParams(TypedDict):
    dataset: List[DatasetItemImage]
    """
    List of image dataset items to classify
    """

    labels: List[LabelItemImage]
    """
    List of labels for classification
    """

    multiple_labels: NotRequired[bool]
    """
    Whether to allow multiple labels per item
    """


class ClassificationResponse(TypedDict):
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

    def text(self, params: ClassificationTextParams) -> ClassificationResponse:
        path = "/classification"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    def image(self, params: ClassificationImageParams) -> ClassificationResponse:
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

    async def text(self, params: ClassificationTextParams) -> ClassificationResponse:
        path = "/classification"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp

    async def image(self, params: ClassificationImageParams) -> ClassificationResponse:
        path = "/classification"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
