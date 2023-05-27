"""
Create tags table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists tags (
                id serial primary key,
                name varchar(30) unique,
                color varchar(30)
            );
        """,
        """
            drop table if exists tags;
        """
    )
]
