from dependency_injector import containers, providers

from app.internal.repositories import Repositories
from .tasks import Tasks
from .tags import  Tags

__all__ = [
    "Services",
    "Tasks",
    "Tags",
]


class Services(containers.DeclarativeContainer):
    repositories = providers.Container(Repositories)
    postgres = providers.Container(repositories.postgres)
    tasks = providers.Singleton(Tasks, tasks=postgres.tasks)
    tags = providers.Singleton(Tags, tags=postgres.tags)
