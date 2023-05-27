"""
Create users_tags table
"""

from yoyo import step

__depends__ = {'20230527_01_nfZ7s-create-tags-table'}

steps = [
    step(
        """
            create table if not exists users_tags(
                tag_id int not null references tags (id) on delete cascade,
                user_id int not null,
                primary key (tag_id, user_id)
            );
        """,
        """
            drop table if exists users_tags;
        """
    )
]
