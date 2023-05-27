from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "UniqueViolation",
    "EmptyResult",
    "DriverError",
    "InvalidDataRequest",
    "EmptyResultResponse",
]


class UniqueViolation(BaseAPIException):
    message = "Not unique"
    status_code = status.HTTP_409_CONFLICT


class EmptyResult(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Empty result"


class InvalidDataRequest(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Invalid data."


class EmptyResultResponse(BaseAPIException):
    message = "Empty result"
    status_code = status.HTTP_404_NOT_FOUND


class DriverError(BaseAPIException):
    def __init__(self, message: str = None):
        if message:
            self.message = message

    message = "Internal error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
