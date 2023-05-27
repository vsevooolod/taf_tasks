### Tasks

GET /tasks/{user_id:int}/ - read all user tasks
GET /tasks/{user_id:int}/{task_id:int}/ - retrieve user task
POST /tasks/{user_id:int}/ - create user task
PATCH /tasks/{user_id:int}/{task_id:int}/ - update user task
DELETE /tasks/{user_id:int}/{task_id:int}/ - delete user task

### Tags

GET /tags/{user_id:int}/ - read all user tags
POST /tags/{user_id:int}/ - create user tag
PATCH /tags/{user_id:int}/{tag_id:int}/ - change tag name
DELETE /tags/{user_id:int}/{tag_id:int}/ - delete user tag
