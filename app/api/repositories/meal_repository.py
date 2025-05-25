from typing import Sequence

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.schemas.meal_schemas import (
    MealListQuery,
    MealCreateSchema,
    MealUpdateSchema,
)
from app.core.databases.postgres import get_general_session
from app.api.models import Meal


class MealRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_meal_by_name(self, name: str) -> Meal | None:
        query = select(Meal).where(Meal.name == name)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def list_meals(self, payload: MealListQuery) -> Sequence[Meal]:
        query = (
            select(Meal).offset((payload.page - 1) * payload.size).limit(payload.size)
        )
        if payload.search:
            query = query.where(Meal.name.ilike(f"%{payload.search}%"))
        result = await self.__session.execute(query)
        return result.scalars().all()

    async def get_meal(self, meal_id: int) -> Meal | None:
        query = select(Meal).where(Meal.id == meal_id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def create_meal(self, payload: MealCreateSchema) -> Meal:
        existing_meal = await self.get_meal_by_name(name=payload.name)
        if existing_meal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Meal with this name already exists.",
            )
        meal = Meal(**payload.model_dump())
        self.__session.add(meal)
        await self.__session.commit()
        await self.__session.refresh(meal)
        return meal

    async def update_meal(self, meal_id: int, payload: MealUpdateSchema) -> Meal:
        meal = await self.get_meal(meal_id=meal_id)
        if not meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )
        existing_meal = await self.get_meal_by_name(name=payload.name)
        if existing_meal and existing_meal.id != meal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Meal with this name already exists.",
            )
        meal.update(**payload.model_dump())
        await self.__session.commit()
        await self.__session.refresh(meal)
        return meal

    async def delete_meal(self, meal_id: int) -> None:
        meal = await self.get_meal(meal_id=meal_id)
        if not meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )
        await self.__session.delete(meal)
        await self.__session.commit()
