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

    async def read(self, user_id: int, task_id: int) -> models.ExtendedTask:
        task = await self._tasks.read(user_id=user_id, task_id=task_id)
        try:
            children = await self._tasks.read_all_children(user_id=user_id, task_id=task_id)
        except EmptyResult:
            children = []
        return models.ExtendedTask(**task.to_dict(), children=children)

    async def create(self, user_id: int, cmd: models.CreateTaskCommand) -> models.Task:
        return await self._tasks.create(user_id=user_id, cmd=cmd)

    async def update(self, user_id: int, task_id: int, cmd: models.UpdateTaskCommand) -> models.Task:
        return await self._tasks.update(user_id=user_id, task_id=task_id, cmd=cmd)

    async def delete(self, user_id: int, task_id: int) -> models.Task:
        return await self._tasks.delete(user_id=user_id, task_id=task_id)

    async def attach_tag(self, **kwargs) -> models.Tag:
        return await self._tasks.attach_tag(**kwargs)

    async def detach_tag(self, **kwargs) -> models.Tag:
        return await self._tasks.detach_tag(**kwargs)
