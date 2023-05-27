from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "CurrencyNotFound",
    "CurrencyUniqueError",
]


class CurrencyNotFound(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = ...


class CurrencyUniqueError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = ...
