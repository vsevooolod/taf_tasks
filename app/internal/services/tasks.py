from typing import List

from app.pkg.logger import Logger, get_logger
from app.internal.repositories import postgres
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg import models

__all__ = [
    "Tasks",
]


class Tasks:
    _logger: Logger
    _tasks: postgres.Tasks

    def __init__(self, tasks: postgres.Tasks):
        self._logger = get_logger(__name__)
        self._tasks = tasks

    async def read_all(self, user_id: int) -> List[models.Task]:
        try:
            return await self._tasks.read_all(user_id=user_id)
        except EmptyResult:
            return []

    async def create(self, user_id: int, cmds: List[models.CreateTaskCommand]) -> List[models.Task]:
        return await self._tasks.create(user_id=user_id, cmds=cmds)

    async def update(self, user_id: int, cmds: List[models.UpdateTaskCommand]) -> List[models.Task]:
        try:
            return await self._tasks.update(user_id=user_id, cmds=cmds)
        except EmptyResult:
            return []

    async def delete(self, user_id: int, cmds: List[models.DeleteTaskCommand]) -> List[models.Task]:
        try:
            return await self._tasks.delete(user_id=user_id, cmds=cmds)
        except EmptyResult:
            return []