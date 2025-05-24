from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

from app.api.schemas.units_schemas import UnitCreateSchema, UnitUpdateSchema
from app.core.databases.postgres import get_general_session
from app.api.models import Unit


class UnitRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_unit_by_code(self, code: str) -> Unit | None:
        result = await self.__session.execute(select(Unit).where(Unit.code == code))
        return result.scalars().first()

    async def get_all_units(self) -> Sequence[Unit]:
        result = await self.__session.execute(select(Unit))
        return result.scalars().all()

    async def get_unit_by_id(self, unit_id: int) -> Unit | None:
        result = await self.__session.execute(select(Unit).where(Unit.id == unit_id))
        return result.scalars().first()

    async def create_unit(self, payload: UnitCreateSchema) -> Unit:
        unit = Unit(**payload.model_dump())
        self.__session.add(unit)
        await self.__session.commit()
        await self.__session.refresh(unit)
        return unit

    async def update_unit(self, unit_id: int, payload: UnitUpdateSchema) -> Unit | None:
        unit = await self.get_unit_by_id(unit_id=unit_id)
        if unit:
            unit.update(**payload.model_dump())
            await self.__session.commit()
            await self.__session.refresh(unit)
            return unit
        return None

    async def delete_unit(self, unit_id: int) -> None:
        unit = await self.get_unit_by_id(unit_id=unit_id)
        if unit:
            await self.__session.delete(unit)
            await self.__session.commit()
