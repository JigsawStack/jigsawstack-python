from jigsawstack.exceptions import JigsawStackError
from jigsawstack import JigsawStack

import pytest

# flake8: noqa

client = JigsawStack()


@pytest.mark.parametrize(
    "dataset,labels",
    [
        (
            [
                {"type": "text", "value": "I love programming"},
                {"type": "text", "value": "I love reading books"},
                {"type": "text", "value": "I love watching movies"},
                {"type": "text", "value": "I love playing games"},
            ],
            [
                {"type": "text", "value": "programming"},
                {"type": "text", "value": "reading"},
                {"type": "text", "value": "watching"},
                {"type": "text", "value": "playing"},
            ],
        ),
        (
            [
                {"type": "text", "value": "This is awesome!"},
                {"type": "text", "value": "I hate this product"},
                {"type": "text", "value": "It's okay, nothing special"},
            ],
            [
                {"type": "text", "value": "positive"},
                {"type": "text", "value": "negative"},
                {"type": "text", "value": "neutral"},
            ],
        ),
        (
            [
                {"type": "text", "value": "The weather is sunny today"},
                {"type": "text", "value": "It's raining heavily outside"},
                {"type": "text", "value": "Snow is falling gently"},
            ],
            [
                {"type": "text", "value": "sunny"},
                {"type": "text", "value": "rainy"},
                {"type": "text", "value": "snowy"},
            ],
        ),
    ],
)
def test_classification_text_success_response(dataset, labels) -> None:
    params = {
        "dataset": dataset,
        "labels": labels,
    }
    try:
        result = client.classification.text(params)
        print(result)
        assert result["success"] == True
    except JigsawStackError as e:
        print(str(e))
        assert e.message == "Failed to parse API response. Please try again."


@pytest.mark.parametrize(
    "dataset,labels",
    [
        (
            [
                {
                    "type": "image",
                    "value": "https://as2.ftcdn.net/v2/jpg/02/24/11/57/1000_F_224115780_2ssvcCoTfQrx68Qsl5NxtVIDFWKtAgq2.jpg",
                },
                {
                    "type": "image",
                    "value": "https://t3.ftcdn.net/jpg/02/95/44/22/240_F_295442295_OXsXOmLmqBUfZreTnGo9PREuAPSLQhff.jpg",
                },
                {
                    "type": "image",
                    "value": "https://as1.ftcdn.net/v2/jpg/05/54/94/46/1000_F_554944613_okdr3fBwcE9kTOgbLp4BrtVi8zcKFWdP.jpg",
                },
            ],
            [
                {"type": "text", "value": "banana"},
                {
                    "type": "image",
                    "value": "https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg",
                },
                {"type": "text", "value": "kisses"},
            ],
        ),
    ],
)
def test_classification_image_success_response(dataset, labels) -> None:
    params = {
        "dataset": dataset,
        "labels": labels,
    }
    try:
        result = client.classification.image(params)
        print(result)
        assert result["success"] == True
    except JigsawStackError as e:
        print(str(e))
        assert e.message == "Failed to parse API response. Please try again."
