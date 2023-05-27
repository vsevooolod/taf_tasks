from typing import List

from app.pkg.models.base import Model
from app.internal.repositories.postgres.handlers.collect_response import collect_response
from app.internal.repositories.repository import Repository
from .connection import get_connection
from app.pkg import models

__all__ = [
    "Tasks",
]


class Tasks(Repository):
    @collect_response
    async def read_all(self, user_id: int) -> List[models.Task]:
        q = """
            select
                id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id
            from tasks
            where user_id = %(user_id)s
              and parent_id is null
            order by deadline, created_at desc;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id})
            return await cur.fetchall()

    @collect_response
    async def read(self, query: Model) -> Model:
        raise NotImplementedError

    @collect_response
    async def create(
            self,
            user_id: int,
            cmd: models.CreateTaskCommand,
    ) -> models.Task:
        params = cmd.to_dict()
        params["user_id"] = user_id
        q = """
            insert into tasks(
                title,
                description,
                deadline,
                user_id,
                parent_id
            ) values (
                %(title)s,
                %(description)s,
                %(deadline)s,
                %(user_id)s,
                %(parent_id)s
            )
            returning
                id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id;
        """
        async with get_connection() as cur:
            await cur.execute(q, params)
            return await cur.fetchone()

    @collect_response
    async def update(
            self,
            user_id: int,
            task_id: int,
            cmd: models.UpdateTaskCommand,
    ) -> models.Task:
        params = cmd.to_dict()
        params["user_id"] = user_id
        params["task_id"] = task_id
        q = """
            update tasks set 
                title = %(title)s,
                description = %(description)s,
                deadline = %(deadline)s::timestamp,
                parent_id = %(parent_id)s::int,
                is_done = %(is_done)s
            where id = %(task_id)s
              and user_id = %(user_id)s
            returning
                id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id;
        """
        async with get_connection() as cur:
            await cur.execute(q, params)
            return await cur.fetchone()

    @collect_response
    async def delete(self, user_id: int, task_id: int) -> models.Task:
        q = """
            delete from tasks
            where user_id = %(user_id)s 
              and id = %(task_id)s
            returning 
                id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id, "task_id": task_id})
            return await cur.fetchone()
