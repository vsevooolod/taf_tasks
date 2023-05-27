from typing import List

from app.pkg.logger import Logger, get_logger
from app.internal.repositories import postgres
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg import models

__all__ = [
    "Tags",
]


class Tags:
    _logger: Logger
    _tags: postgres.Tags

    def __init__(self, tags: postgres.Tags):
        self._logger = get_logger(__name__)
        self._tags = tags

    async def read_all(self, user_id: int) -> List[models.Tag]:
        try:
            return await self._tags.read_all(user_id=user_id)
        except EmptyResult:
            return []

    async def create(self, user_id: int, cmd: models.CreateTagCommand) -> models.Tag:
        return await self._tags.create(user_id=user_id, cmd=cmd)

    async def update(
            self,
            user_id: int,
            tag_id: int,
            cmd: models.UpdateTagCommand,
    ) -> models.Tag:
        return await self._tags.update(user_id=user_id, tag_id=tag_id, cmd=cmd)

    async def delete(self, user_id: int, tag_id: int) -> models.Tag:
        return await self._tags.delete(user_id=user_id, tag_id=tag_id)
