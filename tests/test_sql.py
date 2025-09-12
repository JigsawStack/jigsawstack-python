import logging
import os

import pytest
from dotenv import load_dotenv

import jigsawstack
from jigsawstack.exceptions import JigsawStackError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))

# Sample schemas for different databases
MYSQL_SCHEMA = """
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product_name VARCHAR(255),
    quantity INT,
    price DECIMAL(10, 2),
    order_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

POSTGRESQL_SCHEMA = """
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary NUMERIC(10, 2),
    hire_date DATE,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    budget NUMERIC(12, 2),
    manager_id INTEGER REFERENCES employees(id)
);
"""

SQLITE_SCHEMA = """
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price REAL,
    stock_quantity INTEGER DEFAULT 0
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER,
    sale_date TEXT,
    total_amount REAL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
"""

TEST_CASES = [
    {
        "name": "mysql_simple_select",
        "params": {
            "prompt": "Get all users from the users table",
            "sql_schema": MYSQL_SCHEMA,
            "database": "mysql",
        },
    },
    {
        "name": "mysql_join_query",
        "params": {
            "prompt": "Get all orders with user information for orders placed in the last 30 days",
            "sql_schema": MYSQL_SCHEMA,
            "database": "mysql",
        },
    },
    {
        "name": "mysql_aggregate_query",
        "params": {
            "prompt": "Calculate the total revenue per user",
            "sql_schema": MYSQL_SCHEMA,
            "database": "mysql",
        },
    },
    {
        "name": "postgresql_simple_select",
        "params": {
            "prompt": "Find all active employees",
            "sql_schema": POSTGRESQL_SCHEMA,
            "database": "postgresql",
        },
    },
    {
        "name": "postgresql_complex_join",
        "params": {
            "prompt": "Get all departments with their manager names and department budgets greater than 100000",
            "sql_schema": POSTGRESQL_SCHEMA,
            "database": "postgresql",
        },
    },
    {
        "name": "postgresql_window_function",
        "params": {
            "prompt": "Rank employees by salary within each department",
            "sql_schema": POSTGRESQL_SCHEMA,
            "database": "postgresql",
        },
    },
    {
        "name": "sqlite_simple_query",
        "params": {
            "prompt": "List all products in the electronics category",
            "sql_schema": SQLITE_SCHEMA,
            "database": "sqlite",
        },
    },
    {
        "name": "sqlite_aggregate_with_group",
        "params": {
            "prompt": "Calculate total sales amount for each product",
            "sql_schema": SQLITE_SCHEMA,
            "database": "sqlite",
        },
    },
    {
        "name": "default_database_type",
        "params": {
            "prompt": "Select all records from users table where email contains 'example.com'",
            "sql_schema": MYSQL_SCHEMA,
            # No database specified, should use default
        },
    },
    {
        "name": "complex_multi_table_query",
        "params": {
            "prompt": "Find users who have placed more than 5 orders with total value exceeding 1000",
            "sql_schema": MYSQL_SCHEMA,
            "database": "mysql",
        },
    },
    {
        "name": "insert_query",
        "params": {
            "prompt": "Insert a new user with username 'john_doe' and email 'john@example.com'",
            "sql_schema": MYSQL_SCHEMA,
            "database": "mysql",
        },
    },
    {
        "name": "update_query",
        "params": {
            "prompt": "Update the salary of all employees in the IT department by 10%",
            "sql_schema": POSTGRESQL_SCHEMA,
            "database": "postgresql",
        },
    },
    {
        "name": "delete_query",
        "params": {
            "prompt": "Delete all products with zero stock quantity",
            "sql_schema": SQLITE_SCHEMA,
            "database": "sqlite",
        },
    },
    {
        "name": "subquery_example",
        "params": {
            "prompt": "Find all users who have never placed an order",
            "sql_schema": MYSQL_SCHEMA,
            "database": "mysql",
        },
    },
    {
        "name": "date_filtering",
        "params": {
            "prompt": "Get all employees hired in the last year",
            "sql_schema": POSTGRESQL_SCHEMA,
            "database": "postgresql",
        },
    },
]


class TestSQLSync:
    """Test synchronous SQL text-to-sql methods"""

    sync_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_text_to_sql(self, test_case):
        """Test synchronous text-to-sql with various inputs"""
        try:
            result = jigsaw.text_to_sql(test_case["params"])

            assert result["success"]
            assert "sql" in result
            assert isinstance(result["sql"], str)
            assert len(result["sql"]) > 0

            # Basic SQL validation - check if it contains SQL keywords
            sql_lower = result["sql"].lower()
            sql_keywords = [
                "select",
                "insert",
                "update",
                "delete",
                "create",
                "alter",
                "drop",
            ]
            assert any(keyword in sql_lower for keyword in sql_keywords), (
                "Generated SQL should contain valid SQL keywords"
            )

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestSQLAsync:
    """Test asynchronous SQL text-to-sql methods"""

    async_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_text_to_sql_async(self, test_case):
        """Test asynchronous text-to-sql with various inputs"""
        try:
            result = await async_jigsaw.text_to_sql(test_case["params"])

            assert result["success"]
            assert "sql" in result
            assert isinstance(result["sql"], str)
            assert len(result["sql"]) > 0

            sql_lower = result["sql"].lower()
            sql_keywords = [
                "select",
                "insert",
                "update",
                "delete",
                "create",
                "alter",
                "drop",
            ]
            assert any(keyword in sql_lower for keyword in sql_keywords), (
                "Generated SQL should contain valid SQL keywords"
            )

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
