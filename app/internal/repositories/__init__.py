from dependency_injector import containers, providers

from app.internal.repositories.postgres import Postgres

__all__ = [
    "Repositories",
    "Postgres",
]


class Repositories(containers.DeclarativeContainer):
    postgres = providers.Container(Postgres)
