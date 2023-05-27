from app.pkg.models.base import BaseModel

__all__ = [
    "Tag",
    "CreateTagCommand",
    "UpdateTagCommand",
]


class Tag(BaseModel):
    id: int
    name: str
    color: str


class CreateTagCommand(BaseModel):
    name: str
    color: str


class UpdateTagCommand(CreateTagCommand):
    name: str
    color: str
