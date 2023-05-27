"""
Create tasks table
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
            create table if not exists tasks (
                id serial primary key,
                title varchar(200) not null,
                description varchar(5000),
                deadline timestamp,
                is_done bool default false,
                user_id int not null,
                parent_id int references tasks(id) on delete cascade,
                created_at timestamp default current_timestamp,
                updated_at timestamp default current_timestamp
            );

            create index if not exists user_tasks on tasks(user_id);
            create index if not exists subtasks on tasks(parent_id)
            where parent_id is not null;

            create function update_updated_at_on_tasks()
            returns trigger as $$
            begin
                new.updated_at = current_timestamp;
                return new;
            end;
            $$ language 'plpgsql';

            create trigger update_tasks_updated_at
                before update
                on
                    tasks
                for each row
            execute procedure update_updated_at_on_tasks();
        """,
        """
            drop table if exists tasks;
            drop index if exists user_tasks;
            drop index if exists subtasks;
            drop function update_updated_at_on_tasks;
            drop trigger update_tasks_updated_at;
        """
    )
]
