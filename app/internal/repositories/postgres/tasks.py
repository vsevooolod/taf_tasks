from typing import List

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
                tasks.id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id,
                json_agg(json_strip_nulls(json_build_object(
                    'id', t.id,
                    'name', t.name,
                    'color', t.color
                ))) as tags
            from tasks
            full join tags_on_tasks tot on tasks.id = tot.task_id
            full join tags t on tot.tag_id = t.id
            where user_id = %(user_id)s and parent_id is null
            group by
                tasks.id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id
            order by deadline, created_at desc;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id})
            return await cur.fetchall()

    @collect_response
    async def read(self, user_id: int, task_id: int) -> models.Task:
        q = """
            select
                tasks.id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id,
                json_agg(json_strip_nulls(json_build_object(
                    'id', t.id,
                    'name', t.name,
                    'color', t.color
                ))) as tags
            from tasks
            full join tags_on_tasks tot on tasks.id = tot.task_id
            full join tags t on tot.tag_id = t.id
            where user_id = %(user_id)s and tasks.id = %(task_id)s
            group by
                tasks.id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id
            order by deadline, created_at desc;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id, "task_id": task_id})
            return await cur.fetchone()

    @collect_response
    async def read_all_children(self, user_id: int, task_id: int) -> List[models.Task]:
        q = """
            select
                tasks.id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id,
                json_agg(json_strip_nulls(json_build_object(
                    'id', t.id,
                    'name', t.name,
                    'color', t.color
                ))) as tags
            from tasks
            full join tags_on_tasks tot on tasks.id = tot.task_id
            full join tags t on tot.tag_id = t.id
            where user_id = %(user_id)s and parent_id = %(task_id)s
            group by
                tasks.id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id
            order by deadline, created_at desc;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id, "task_id": task_id})
            return await cur.fetchall()

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
                parent_id,
                '[]'::json as tags;
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
            where id = %(task_id)s and user_id = %(user_id)s
            returning
                id,
                title,
                description,
                deadline,
                is_done,
                created_at,
                updated_at,
                user_id,
                parent_id,
                (select
                    json_agg(json_strip_nulls(json_build_object(
                        'id', t.id,
                        'name', t.name,
                        'color', t.color
                    )))
                from tags t
                full join tags_on_tasks tot on t.id = tot.tag_id
                group by tot.task_id
                ) as tags;
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
                parent_id,
                (select
                    json_agg(json_strip_nulls(json_build_object(
                        'id', t.id,
                        'name', t.name,
                        'color', t.color
                    )))
                from tags t
                full join tags_on_tasks tot on t.id = tot.tag_id
                group by tot.task_id
                ) as tags;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id, "task_id": task_id})
            return await cur.fetchone()

    @collect_response
    async def attach_tag(
            self,
            user_id: int,
            task_id: int,
            tag_id: int,
    ) -> models.Tag:
        q = """
            insert into tags_on_tasks (tag_id, task_id)
            select %(tag_id)s, %(task_id)s from tasks
            where tasks.id = %(task_id)s
              and tasks.user_id = %(user_id)s
            on conflict (tag_id, task_id) do update set
              tag_id = excluded.tag_id,
              task_id = excluded.task_id
            returning
                (select id from tags where id = %(tag_id)s),
                (select name from tags where id = %(tag_id)s),
                (select color from tags where id = %(tag_id)s);
        """
        async with get_connection() as cur:
            await cur.execute(q, {
                "user_id": user_id,
                "task_id": task_id,
                "tag_id": tag_id,
            })
            return await cur.fetchone()

    @collect_response
    async def detach_tag(
            self,
            user_id: int,
            task_id: int,
            tag_id: int,
    ) -> models.Tag:
        q = """
            delete from tags_on_tasks
            using tasks
            where task_id = %(task_id)s 
              and tag_id = %(tag_id)s
              and tasks.id = %(task_id)s
              and tasks.user_id = %(user_id)s
            returning 
                (select id from tags where id = %(tag_id)s),
                (select name from tags where id = %(tag_id)s),
                (select color from tags where id = %(tag_id)s);
        """
        async with get_connection() as cur:
            await cur.execute(q, {
                "user_id": user_id,
                "task_id": task_id,
                "tag_id": tag_id,
            })
            return await cur.fetchone()
