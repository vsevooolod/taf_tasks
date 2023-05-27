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
    description="Read all user tasks",
)
@inject
async def read_all(
        user_id: int,
        service: Tasks = Depends(Provide[Services.tasks]),
) -> List[models.Task]:
    return await service.read_all(user_id=user_id)


# @router.get(
#     path="/{user_id:int}/{task_id:int}/",
# )


@router.post(
    path="/{user_id:int}/",
    response_model=models.Task,
    status_code=status.HTTP_201_CREATED,
    description="Create user task",
)
@inject
async def create(
        user_id: int,
        cmd: models.CreateTaskCommand,
        service: Tasks = Depends(Provide[Services.tasks]),
) -> models.Task:
    return await service.create(user_id=user_id, cmd=cmd)


@router.patch(
    path="/{user_id:int}/{task_id:int}/",
    response_model=models.Task,
    status_code=status.HTTP_200_OK,
    description="Update user task",
)
@inject
async def update(
        user_id: int,
        task_id: int,
        cmd: models.UpdateTaskCommand,
        service: Tasks = Depends(Provide[Services.tasks]),
) -> models.Task:
    return await service.update(user_id=user_id, task_id=task_id, cmd=cmd)


@router.delete(
    path="/{user_id:int}/{task_id:int}/",
    response_model=models.Task,
    status_code=status.HTTP_200_OK,
    description="Delete user task",
)
@inject
async def delete(
        user_id: int,
        task_id: int,
        service: Tasks = Depends(Provide[Services.tasks]),
) -> models.Task:
    return await service.delete(user_id=user_id, task_id=task_id)
