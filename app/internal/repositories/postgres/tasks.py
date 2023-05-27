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
    async def create(self, user_id: int, cmds: List[models.CreateTaskCommand]) -> List[models.Task]:
        params = {"values": []}
        for cmd in cmds:
            cmd.user_id = user_id
            params["values"].append(cmd.to_string())
        params["values"] = ", ".join(params["values"])
        q = """
            insert into tasks(
                title,
                description,
                deadline,
                user_id,
                parent_id
            ) values %(values)s
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
            await cur.execute(q % params)
            return await cur.fetchall()

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
            order by deadline, created_at desc;
        """
        async with get_connection() as cur:
            await cur.execute(q % {"user_id": user_id})
            return await cur.fetchall()

    @collect_response
    async def update(self, user_id: int, cmds: List[models.UpdateTaskCommand]) -> List[models.Task]:
        params = {"values": []}
        for cmd in cmds:
            cmd.user_id = user_id
            params["values"].append(cmd.to_string())
        params["values"] = ", ".join(params["values"])
        q = """
            update tasks set 
                title = tmp.title,
                description = tmp.description,
                deadline = tmp.deadline::timestamp,
                parent_id = tmp.parent_id::int,
                is_done = tmp.is_done
            from (values %(values)s) as tmp(
                id, 
                user_id,
                title, 
                description, 
                deadline, 
                parent_id, 
                is_done
            )
            where tasks.id = tmp.id 
              and tasks.user_id = tmp.user_id
            returning
                tasks.id,
                tasks.title,
                tasks.description,
                tasks.deadline,
                tasks.is_done,
                created_at,
                updated_at,
                tasks.user_id,
                tasks.parent_id;
        """
        async with get_connection() as cur:
            await cur.execute(q % params)
            return await cur.fetchall()

    @collect_response
    async def delete(self, user_id: int, cmds: List[models.DeleteTaskCommand]) -> List[models.Task]:
        params = {"bundles": [f"'{user_id}-{cmd.id}'" for cmd in cmds]}
        params["bundles"] = ", ".join(params["bundles"])
        q = """
            delete from tasks
            where user_id::varchar || '-' || id::varchar in (%(bundles)s)
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
            await cur.execute(q % params)
            return await cur.fetchall()

    async def read(self, query: Model) -> Model:
        raise NotImplementedError
