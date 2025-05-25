from fastapi import APIRouter, Depends, status, HTTPException

from app.api.controllers import UnitController
from app.api.models import User
from app.api.schemas.units_schemas import (
    UnitReadSchema,
    UnitCreateSchema,
    UnitUpdateSchema,
)
from app.core.utils.security import get_current_user

router = APIRouter(
    prefix="/units",
    tags=["units"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UnitReadSchema],
)
async def get_all_units(
    unit_controller: UnitController = Depends(),
    current_user: User = Depends(get_current_user),
) -> list[UnitReadSchema]:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await unit_controller.get_all_units()


@router.get(
    "/{unit_id}",
    status_code=status.HTTP_200_OK,
    response_model=UnitReadSchema,
)
async def get_unit_by_id(
    unit_id: int,
    current_user: User = Depends(get_current_user),
    unit_controller: UnitController = Depends(),
) -> UnitReadSchema:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await unit_controller.get_unit_by_id(unit_id=unit_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UnitReadSchema)
async def create_unit(
    payload: UnitCreateSchema,
    unit_controller: UnitController = Depends(),
    current_user: User = Depends(get_current_user),
) -> UnitReadSchema:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await unit_controller.create_unit(payload=payload)


@router.put(
    "/{unit_id}/", status_code=status.HTTP_200_OK, response_model=UnitReadSchema
)
async def update_unit(
    unit_id: int,
    payload: UnitUpdateSchema,
    current_user: User = Depends(get_current_user),
    unit_controller: UnitController = Depends(),
) -> UnitReadSchema:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await unit_controller.update_unit(unit_id=unit_id, payload=payload)


@router.delete("/{unit_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit(
    unit_id: int,
    current_user: User = Depends(get_current_user),
    unit_controller: UnitController = Depends(),
) -> None:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await unit_controller.delete_unit(unit_id=unit_id)
