from typing import Any, Dict, List, Union, cast
from typing_extensions import NotRequired, TypedDict
from .request import Request
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
    def text_to_sql(self, params: SQLParams) -> SQLResponse:
        path = "/ai/sql"
        resp = Request(
            api_key=self.api_key,
            api_url=self.api_url,
            path=path,params=cast(Dict[Any, Any], params),verb="post").perform_with_content()
        return resp