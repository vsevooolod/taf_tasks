"""
Create tags_on_tasks table
"""

from yoyo import step

__depends__ = {'20230527_01_nfZ7s-create-tags-table', '20230514_01_2F6aE-create-tasks-table'}

steps = [
    step(
        """
            create table if not exists tags_on_tasks (
                tag_id int references tags (id) on delete cascade,
                task_id int references tasks (id) on delete cascade,
                primary key (tag_id, task_id)
            );
        """,
        """
            drop table if exists tags_on_tasks;
        """
    )
]
