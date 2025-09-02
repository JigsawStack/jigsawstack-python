from typing_extensions import NotRequired, TypedDict


class UsageInfo(TypedDict):
    input_tokens: int
    output_tokens: int
    inference_time_tokens: int
    total_tokens: int


class BaseResponse(TypedDict):
    success: bool
    _usage: NotRequired[UsageInfo]
