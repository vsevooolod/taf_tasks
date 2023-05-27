from dependency_injector import containers, providers

from app.internal.repositories.postgres.connection import get_connection
from .tasks import Tasks
from .tags import Tags

__all__ = [
    "get_connection",
    "Postgres",
    "Tasks",
    "Tags",
]


class Postgres(containers.DeclarativeContainer):
    tasks = providers.Factory(Tasks)
    tags = providers.Factory(Tags)
