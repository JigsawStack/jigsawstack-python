from jigsawstack.exceptions import JigsawStackError
import jigsawstack
import pytest
import logging
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jigsaw = jigsawstack.JigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))
async_jigsaw = jigsawstack.AsyncJigsawStack(api_key=os.getenv("JIGSAWSTACK_API_KEY"))



def generate_dates(start_date, num_days):
    dates = []
    for i in range(num_days):
        date = start_date + timedelta(days=i)
        dates.append(date.strftime("%Y-%m-%d %H:%M:%S"))
    return dates


start = datetime(2024, 1, 1)
dates = generate_dates(start, 30)
dates = [str(date) for date in dates]

TEST_CASES = [
    {
        "name": "linear_growth_pattern",
        "params": {
            "dataset": [{"date": dates[i], "value": 100 + (i * 10)} for i in range(10)],
            "steps": 5,
        },
    },
    {
        "name": "exponential_growth_pattern",
        "params": {
            "dataset": [{"date": dates[i], "value": 100 * (1.1**i)} for i in range(10)],
            "steps": 3,
        },
    },
    {
        "name": "seasonal_pattern",
        "params": {
            "dataset": [
                {"date": dates[i], "value": 100 + (50 * (i % 7))} for i in range(21)
            ],
            "steps": 7,
        },
    },
    {
        "name": "single_step_prediction",
        "params": {
            "dataset": [{"date": dates[i], "value": 200 + (i * 5)} for i in range(15)],
            "steps": 1,
        },
    },
    {
        "name": "large_dataset_prediction",
        "params": {
            "dataset": [
                {"date": dates[i], "value": 1000 + (i * 20)} for i in range(30)
            ],
            "steps": 10,
        },
    },
    {
        "name": "declining_trend",
        "params": {
            "dataset": [{"date": dates[i], "value": 500 - (i * 10)} for i in range(10)],
            "steps": 5,
        },
    },
    {
        "name": "volatile_data",
        "params": {
            "dataset": [
                {"date": dates[0], "value": 100},
                {"date": dates[1], "value": 150},
                {"date": dates[2], "value": 80},
                {"date": dates[3], "value": 200},
                {"date": dates[4], "value": 120},
                {"date": dates[5], "value": 180},
                {"date": dates[6], "value": 90},
                {"date": dates[7], "value": 160},
            ],
            "steps": 4,
        },
    },
    {
        "name": "constant_values",
        "params": {
            "dataset": [{"date": dates[i], "value": 100} for i in range(10)],
            "steps": 3,
        },
    },
    {
        "name": "string_values_prediction",
        "params": {
            "dataset": [
                {"date": dates[0], "value": "33.4"},
                {"date": dates[1], "value": "33.6"},
                {"date": dates[2], "value": "33.6"},
                {"date": dates[3], "value": "33.0"},
                {"date": dates[4], "value": "265.0"},
                {"date": dates[5], "value": "80"},
                {"date": dates[6], "value": "90.45"},
            ],
            "steps": 3,
        },
    },
    {
        "name": "minimal_dataset",
        "params": {
            "dataset": [
                {"date": dates[0], "value": 50},
                {"date": dates[1], "value": 60},
                {"date": dates[2], "value": 70},
                {"date": dates[3], "value": 80},
                {"date": dates[4], "value": 90},
            ],
            "steps": 2,
        },
    },
]


class TestPredictionSync:
    """Test synchronous prediction methods"""

    sync_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", sync_test_cases, ids=[tc["name"] for tc in sync_test_cases]
    )
    def test_prediction(self, test_case):
        """Test synchronous prediction with various inputs"""
        try:
            result = jigsaw.prediction(test_case["params"])

            assert result["success"]
            assert "prediction" in result
            assert isinstance(result["prediction"], list)

            # Verify the number of predictions matches the requested steps
            assert len(result["prediction"]) == test_case["params"]["steps"]

            # Verify each prediction has the required fields
            for prediction in result["prediction"]:
                assert "date" in prediction
                assert "value" in prediction

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")


class TestPredictionAsync:
    """Test asynchronous prediction methods"""

    async_test_cases = TEST_CASES

    @pytest.mark.parametrize(
        "test_case", async_test_cases, ids=[tc["name"] for tc in async_test_cases]
    )
    @pytest.mark.asyncio
    async def test_prediction_async(self, test_case):
        """Test asynchronous prediction with various inputs"""
        try:
            result = await async_jigsaw.prediction(test_case["params"])

            assert result["success"]
            assert "prediction" in result
            assert isinstance(result["prediction"], list)

            # Verify the number of predictions matches the requested steps
            assert len(result["prediction"]) == test_case["params"]["steps"]

            # Verify each prediction has the required fields
            for prediction in result["prediction"]:
                assert "date" in prediction
                assert "value" in prediction

        except JigsawStackError as e:
            pytest.fail(f"Unexpected JigsawStackError in {test_case['name']}: {e}")
