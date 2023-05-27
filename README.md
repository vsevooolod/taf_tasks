### Tasks

* GET /tasks/{user_id:int}/ [Read all user tasks]
* GET /tasks/{user_id:int}/{task_id:int}/ [Retrieve user task]
* POST /tasks/{user_id:int}/ [Create user task]
* PATCH /tasks/{user_id:int}/{task_id:int}/ [Update user task]
* DELETE /tasks/{user_id:int}/{task_id:int}/ [Delete user task]

### Tags

* GET /tags/{user_id:int}/ [Read all user tags]
* POST /tags/{user_id:int}/ [Create user tag]
* PATCH /tags/{user_id:int}/{tag_id:int}/ [Change tag name or color]
* DELETE /tags/{user_id:int}/{tag_id:int}/ [Delete user tag]

### TODO

* Расширить логику взаимодействия с задачами, добавив возможность навешивания тегов
