from typing import List

from app.pkg.models.base import Model
from app.internal.repositories.postgres.handlers.collect_response import collect_response
from app.internal.repositories.repository import Repository
from .connection import get_connection
from app.pkg import models

__all__ = [
    "Tags",
]


class Tags(Repository):
    @collect_response
    async def read_all(self, user_id: int) -> List[models.Tag]:
        q = """
            select
                id,
                name,
                color
            from tags
            join users_tags ut on tags.id = ut.tag_id
            where ut.user_id = %(user_id)s
            order by name;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id})
            return await cur.fetchall()

    @collect_response
    async def create(
            self,
            user_id: int,
            cmd: models.CreateTagCommand,
    ) -> models.Tag:
        params = cmd.to_dict()
        params["user_id"] = user_id
        q = """
            with created as (
                insert into tags (name, color)
                values (%(name)s, %(color)s)
                on conflict (name) do update set
                    color = excluded.color
                returning id, name, color
            )
            insert into users_tags (tag_id, user_id)
            select created.id, %(user_id)s from created
            on conflict (tag_id, user_id) do update set
                tag_id = excluded.tag_id,
                user_id = excluded.user_id
            returning
                (select id from created),
                (select name from created),
                (select color from created);
        """
        async with get_connection() as cur:
            await cur.execute(q, params)
            return await cur.fetchone()

    @collect_response
    async def update(
            self,
            user_id: int,
            tag_id: int,
            cmd: models.UpdateTagCommand,
    ) -> models.Tag:
        params = cmd.to_dict()
        params["user_id"], params["tag_id"] = user_id, tag_id
        q = """
            update tags 
            set name = %(name)s,
                color = %(color)s
            from users_tags
            where users_tags.tag_id = %(tag_id)s
              and users_tags.user_id = %(user_id)s
              and tags.id = %(tag_id)s
            returning id, name, color;     
        """
        async with get_connection() as cur:
            await cur.execute(q, params)
            return await cur.fetchone()

    @collect_response
    async def delete(self, user_id: int, tag_id: int) -> models.Tag:
        q = """
            delete from tags
            using users_tags
            where tags.id = %(tag_id)s
              and users_tags.user_id = %(user_id)s
              and users_tags.tag_id = %(tag_id)s
            returning id, name, color;
        """
        async with get_connection() as cur:
            await cur.execute(q, {"user_id": user_id, "tag_id": tag_id})
            return await cur.fetchone()

    async def read(self, query: Model) -> Model:
        raise NotImplementedError
