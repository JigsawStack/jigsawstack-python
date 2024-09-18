from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request, RequestConfig
from typing import List, Union
from ._config import ClientConfig


class SQLParams(TypedDict):
    prompt: str
    """
    The prompt that will be translated to an SQL query.
    """

    sql_schema: NotRequired[str]

    """
    The database schema where the query will be run. Not required if file_store_key is specified.
    """

    file_store_key: NotRequired[str]
    """
    The key used to store the database schema on Jigsawstack file Storage. Not required if sql_schema is specified.
    """


class SQLResponse(TypedDict):
    success: bool
    """
    Indicates whether the translation was successful.
    """
    sql: str
    """
    The SQL statement.
    """


class SQL(ClientConfig):

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

    def text_to_sql(self, params: SQLParams) -> SQLResponse:
        path = "/ai/sql"
        resp = Request(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
