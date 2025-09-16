from typing import Any, Dict, Literal, Union, cast

from typing_extensions import NotRequired, TypedDict

from ._config import ClientConfig
from ._types import BaseResponse
from .async_request import AsyncRequest
from .request import Request, RequestConfig


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
    database: NotRequired[Literal["mysql", "postgresql", "sqlite"]]
    """
    The type of database for the SQL query (mysql, postgresql, sqlite).
    """


class SQLResponse(BaseResponse):
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
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, api_url, headers)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            headers=headers,
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


class AsyncSQL(ClientConfig):
    config: RequestConfig

    def __init__(
        self,
        api_key: str,
        api_url: str,
        headers: Union[Dict[str, str], None] = None,
    ):
        super().__init__(api_key, api_url, headers)
        self.config = RequestConfig(
            api_url=api_url,
            api_key=api_key,
            headers=headers,
        )

    async def text_to_sql(self, params: SQLParams) -> SQLResponse:
        path = "/ai/sql"
        resp = await AsyncRequest(
            config=self.config,
            path=path,
            params=cast(Dict[Any, Any], params),
            verb="post",
        ).perform_with_content()
        return resp
