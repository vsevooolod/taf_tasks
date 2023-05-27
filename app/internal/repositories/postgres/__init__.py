from dependency_injector import containers, providers

from app.internal.repositories.postgres.connection import get_connection
from .tasks import Tasks

__all__ = [
    "get_connection",
    "Postgres",
    "Tasks",
]


class Postgres(containers.DeclarativeContainer):
    tasks = providers.Factory(Tasks)
