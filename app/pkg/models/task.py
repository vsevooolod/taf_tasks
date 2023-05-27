from typing import Optional
from datetime import datetime

from app.pkg.models.base import BaseModel

__all__ = [
    "Task",
    "CreateTaskCommand",
    "UpdateTaskCommand",
    "DeleteTaskCommand",
]


class CreateTaskCommand(BaseModel):
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    user_id: Optional[int]
    parent_id: Optional[int]


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    is_done: bool
    created_at: datetime
    updated_at: datetime
    user_id: Optional[int]
    parent_id: Optional[int]


class UpdateTaskCommand(BaseModel):
    id: int
    user_id: Optional[int]
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    parent_id: Optional[int]
    is_done: bool


class DeleteTaskCommand(BaseModel):
    id: int
    user_id: Optional[int]
