from dependency_injector import containers, providers

from app.internal.repositories import Repositories
from .tasks import Tasks

__all__ = [
    "Services",
    "Tasks",
]


class Services(containers.DeclarativeContainer):
    repositories = providers.Container(Repositories)
    postgres = providers.Container(repositories.postgres)
    tasks = providers.Singleton(
        Tasks,
        tasks=postgres.tasks,
    )
