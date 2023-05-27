from typing import List

from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject

from app.internal.services import Services, Tags
from app.pkg import models

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get(
    path="/{user_id:int}/",
    response_model=List[models.Tag],
    status_code=status.HTTP_200_OK,
    description="Read all user tags",
)
@inject
async def read_all(
        user_id: int,
        service: Tags = Depends(Provide[Services.tags]),
) -> List[models.Tag]:
    return await service.read_all(user_id=user_id)


@router.post(
    path="/{user_id:int}/",
    response_model=models.Tag,
    status_code=status.HTTP_201_CREATED,
    description="Create user tag",
)
@inject
async def create(
        user_id: int,
        cmd: models.CreateTagCommand,
        service: Tags = Depends(Provide[Services.tags]),
) -> models.Tag:
    return await service.create(user_id=user_id, cmd=cmd)


@router.patch(
    path="/{user_id:int}/{tag_id:int}/",
    response_model=models.Tag,
    status_code=status.HTTP_200_OK,
    description="Update user tag",
)
@inject
async def update(
        user_id: int,
        tag_id: int,
        cmd: models.UpdateTagCommand,
        service: Tags = Depends(Provide[Services.tags]),
) -> models.Tag:
    return await service.update(user_id=user_id, tag_id=tag_id, cmd=cmd)


@router.delete(
    path="/{user_id:int}/{tag_id:int}/",
    response_model=models.Tag,
    status_code=status.HTTP_200_OK,
    description="Delete user tag",
)
@inject
async def delete(
        user_id: int,
        tag_id: int,
        service: Tags = Depends(Provide[Services.tags]),
) -> models.Tag:
    return await service.delete(user_id=user_id, tag_id=tag_id)
