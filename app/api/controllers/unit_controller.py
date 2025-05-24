from fastapi import Depends, HTTPException, status

from app.api.repositories import UnitRepository
from app.api.schemas.units_schemas import (
    UnitReadSchema,
    UnitCreateSchema,
    UnitUpdateSchema,
)


class UnitController:
    def __init__(self, unit_repository: UnitRepository = Depends()):
        self.__unit_repository = unit_repository

    async def get_all_units(self) -> list[UnitReadSchema]:
        units = await self.__unit_repository.get_all_units()
        if not units:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Units are not available yet",
            )
        return [UnitReadSchema.model_validate(unit) for unit in units]

    async def get_unit_by_id(self, unit_id: int) -> UnitReadSchema:
        unit = await self.__unit_repository.get_unit_by_id(unit_id=unit_id)
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unit with id {unit_id} not found",
            )
        return UnitReadSchema.model_validate(unit)

    async def create_unit(self, payload: UnitCreateSchema) -> UnitReadSchema:
        existing_unit = await self.__unit_repository.get_unit_by_code(code=payload.code)

        if existing_unit is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unit with code {payload.code} already exists",
            )
        unit = await self.__unit_repository.create_unit(payload=payload)
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unit creation failed",
            )
        return UnitReadSchema.model_validate(unit)

    async def update_unit(
        self, unit_id: int, payload: UnitUpdateSchema
    ) -> UnitReadSchema:
        unit = await self.__unit_repository.update_unit(
            unit_id=unit_id, payload=payload
        )
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unit with id {unit_id} not found",
            )
        return UnitReadSchema.model_validate(unit)

    async def delete_unit(self, unit_id: int) -> None:
        unit = await self.__unit_repository.get_unit_by_id(unit_id=unit_id)
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unit with id {unit_id} not found",
            )
        await self.__unit_repository.delete_unit(unit_id=unit_id)
