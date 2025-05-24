from fastapi import APIRouter, Depends, status

from app.api.controllers import UnitController
from app.api.schemas.units_schemas import UnitReadSchema, UnitCreateSchema

router = APIRouter(
    prefix="/units",
    tags=["units"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UnitReadSchema],
)
async def get_all_units(
    unit_controller: UnitController = Depends(),
) -> list[UnitReadSchema]:
    return await unit_controller.get_all_units()


@router.get(
    "/{unit_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UnitReadSchema,
)
async def get_unit_by_id(
    unit_id: int,
    unit_controller: UnitController = Depends(),
) -> UnitReadSchema:
    return await unit_controller.get_unit_by_id(unit_id=unit_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UnitCreateSchema)
async def create_unit(
    payload: UnitCreateSchema,
    unit_controller: UnitController = Depends(),
) -> UnitReadSchema:
    return await unit_controller.create_unit(payload=payload)


@router.delete("/{unit_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit(
    unit_id: int,
    unit_controller: UnitController = Depends(),
) -> None:
    return await unit_controller.delete_unit(unit_id=unit_id)
