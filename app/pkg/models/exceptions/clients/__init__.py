from fastapi import status

from app.pkg.models.base.exception import BaseAPIException

__all__ = [
    "ClientException",
]


class ClientException(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
