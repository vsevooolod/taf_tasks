from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "BoostNotFound",
    "BoostUniqueError",
    "BoostError",
]


class BoostNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = ...


class BoostUniqueError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = ...


class BoostError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = ...
