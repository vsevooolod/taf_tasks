from typing import Optional, List
from datetime import datetime

from pydantic import validator

from app.pkg.models.base import BaseModel
from .tag import Tag

__all__ = [
    "Task",
    "ExtendedTask",
    "CreateTaskCommand",
    "UpdateTaskCommand",
]


class CreateTaskCommand(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    parent_id: Optional[int]


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    is_done: bool
    created_at: datetime
    updated_at: datetime
    user_id: int
    parent_id: Optional[int]
    tags: List[Tag]

    @validator("tags", pre=True)
    def if_tags_is_empty(cls, v: List[Tag]) -> List[Tag]:
        if isinstance(v, list) and len(v) > 0 and not v[0]:
            return []
        return v


class ExtendedTask(Task):
    children: List[Task]


class UpdateTaskCommand(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    parent_id: Optional[int]
    is_done: bool
