from typing import Optional
from datetime import datetime

from app.pkg.models.base import BaseModel

__all__ = [
    "Task",
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


class UpdateTaskCommand(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    parent_id: Optional[int]
    is_done: bool
