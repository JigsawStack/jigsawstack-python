"""JigsawStack Exceptions module.

This module defines the base types for platform-wide error

"""

from typing import Any, Dict, Union


class JigsawStackError(Exception):
    """Base class for all errors raised by JigsawStack SDK.
    This is the parent class of all exceptions (server side)
    raised by the JigsawStack SDK. Developers can simply catch
    this class and inspect its `code` to implement more specific
    error handling. Note that for some client-side errors ie:
    some method argument missing, a ValueError would be raised.

    Args:
        code: A string error indicating the HTTP status code
        attributed to that Error.
        message: A human-readable error message string.
        suggested_action: A suggested action path to help the user.
        error_type: Maps to the `type` field from the JigsawStack API
    """

    def __init__(
        self,
        code: Union[str, int],
        message: str,
        suggested_action: str,
        err: Union[str, Dict[str, Any]] = None,
    ):
        Exception.__init__(self, message)
        self.code = code
        self.message = message
        self.suggested_action = suggested_action
        self.error = err
        self.success = False


class MissingApiKeyError(JigsawStackError):

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
    ):
        suggested_action = """Include the following header
        Authorization: Bearer YOUR_API_KEY in the request."""

        message = "Missing API key in the authorization header."

        JigsawStackError.__init__(
            self,
            message=message,
            suggested_action=suggested_action,
            code=code,
            error_type=error_type,
        )


class InvalidApiKeyError(JigsawStackError):
   

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
    ):
        suggested_action = """Generate a new API key in the dashboard."""

        JigsawStackError.__init__(
            self,
            message=message,
            suggested_action=suggested_action,
            code=code,
            error_type=error_type,
        )


class ValidationError(JigsawStackError):


    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
    ):
        default_message = """
        The request body is missing one or more required fields."""

        suggested_action = """Check the error message
        to see the list of missing fields."""

        if message == "":
            message = default_message

        JigsawStackError.__init__(
            self,
            code=code or "400",
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
        )


class MissingRequiredFieldsError(JigsawStackError):

    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
    ):
        default_message = """
        The request body is missing one or more required fields."""

        suggested_action = """Check the error message
        to see the list of missing fields."""

        if message == "":
            message = default_message

        JigsawStackError.__init__(
            self,
            code=code or "422",
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
        )


class ApplicationError(JigsawStackError):


    def __init__(
        self,
        message: str,
        error_type: str,
        code: Union[str, int],
    ):
        default_message = """
        Something went wrong."""

        suggested_action = """Contact JigsawStack support."""

        if message == "":
            message = default_message

        JigsawStackError.__init__(
            self,
            code=code or "500",
            message=message,
            suggested_action=suggested_action,
            error_type=error_type,
        )


# Dict with error code -> error type mapping
ERRORS: Dict[str, Dict[str, Any]] = {
    "400": {"validation_error": ValidationError},
    "422": {
        "missing_required_fields": MissingRequiredFieldsError,
        "validation_error": ValidationError,
    },
    "401": {"missing_api_key": MissingApiKeyError},
    "403": {"invalid_api_key": InvalidApiKeyError},
    "500": {"application_error": ApplicationError},
}


def raise_for_code_and_type(
    code: Union[str, int], message: str, err : Union[str, Dict[str, Any]] = None
) -> None:
    """Raise the appropriate error based on the code and type.

    Args:
        code (str): The error code
        error_type (str): The error type
        message (str): The error message

    Raises:
        JigsawStackError: If it is a JigsawStack err
            or
        ValidationError: If the error type is validation_error
            or
        MissingRequiredFieldsError: If the error type is missing_required_fields
            or
        MissingApiKeyError: If the error type is missing_api_key
            or
        InvalidApiKeyError: If the error type is invalid_api_key
            or
        ApplicationError: If the error type is application_error
            or
        TypeError: If the error type is not found
    """
    error = ERRORS.get(str(code))

    # Handle the case where the error might be unknown
    if error is None:
        raise JigsawStackError(
            code=code, message=message, err=err, suggested_action=""
        )

    # defaults to JigsawStackError if finally can't find error type
    raise JigsawStackError(
        code=code, message=message, err=err,  suggested_action=""
    )


class NoContentError(Exception):
    """Raised when the response body is empty."""

    def __init__(self) -> None:
        self.message = """No content was returned from the API.
            Please contact Jigsawstack support."""
        Exception.__init__(self, self.message)