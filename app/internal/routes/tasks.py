from typing import List

from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import Provide, inject

from app.internal.services import Services, Tasks
from app.pkg import models

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get(
    path="/{user_id:int}/",
    response_model=List[models.Task],
    status_code=status.HTTP_200_OK,
    description="Read all tasks",
)
@inject
async def read_all(
        user_id: int,
        service: Tasks = Depends(Provide[Services.tasks]),
) -> List[models.Task]:
    return await service.read_all(user_id=user_id)


@router.post(
    path="/{user_id:int}/",
    response_model=List[models.Task],
    status_code=status.HTTP_200_OK,
    description="Create tasks",
)
@inject
async def create(
        user_id: int,
        cmds: List[models.CreateTaskCommand],
        service: Tasks = Depends(Provide[Services.tasks]),
) -> List[models.Task]:
    return await service.create(user_id=user_id, cmds=cmds)


@router.patch(
    path="/{user_id:int}/",
    response_model=List[models.Task],
    status_code=status.HTTP_200_OK,
    description="Update tasks",
)
@inject
async def update(
        user_id: int,
        cmds: List[models.UpdateTaskCommand],
        service: Tasks = Depends(Provide[Services.tasks]),
) -> List[models.Task]:
    return await service.update(user_id=user_id, cmds=cmds)


@router.delete(
    path="/{user_id:int}/",
    response_model=List[models.Task],
    status_code=status.HTTP_201_CREATED,
    description="Delete tasks",
)
@inject
async def delete(
        user_id: int,
        cmds: List[models.DeleteTaskCommand],
        service: Tasks = Depends(Provide[Services.tasks]),
) -> List[models.Task]:
    return await service.delete(user_id=user_id, cmds=cmds)
