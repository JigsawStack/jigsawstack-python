from unittest.mock import MagicMock
import unittest

from jigsawstack.exceptions import JigsawStackError

import jigsawstack
import jigsawstack.sentiment
import jigsawstack.sentiment._sentiment
import jigsawstack.sql
import jigsawstack.sql._sql
import jigsawstack.translate
import jigsawstack.translate._translate
import pytest
# flake8: noqa

@pytest.mark.skip(reason="Skipping TestWebAPI class for now")
class TestTextToSQLAPI(unittest.TestCase):

    def test_sql_response_success(self) -> None:
        params = {
            "prompt": "Generate a query to get transactions that amount exceed 10000 and sort by when created",
            "sql_schema": "CREATE TABLE Transactions (transaction_id INT PRIMARY KEY, user_id INT NOT NULL,total_amount DECIMAL(10, 2 NOT NULL, transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,status VARCHAR(20) DEFAULT 'pending',FOREIGN KEY(user_id) REFERENCES Users(user_id))"
        }
        try:
            result = jigsawstack.SQL.text_to_sql(params)
            assert result["success"] == True
        except JigsawStackError as e:
            assert e.message == "Failed to parse API response. Please try again."