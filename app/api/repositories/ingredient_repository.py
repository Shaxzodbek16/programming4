from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends
from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.api.schemas.ingredients_schemas import (
    IngredientListQuery,
    IngredientCreateSchema,
    IngredientUpdateSchema,
)
from app.core.databases.postgres import get_general_session
from app.api.models import Ingredient


class IngredientRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_ingredient_by_name(self, name: str) -> Ingredient | None:
        result = await self.__session.execute(
            select(Ingredient).where(Ingredient.name.ilike(f"{name}"))
        )
        return result.scalar_one_or_none()

    async def get_all_ingredients(
        self, payload: IngredientListQuery
    ) -> Sequence[Ingredient]:
        query = (
            select(Ingredient)
            .offset((payload.page - 1) * payload.size)
            .limit(payload.size)
        )
        if payload.search:
            query = query.where(Ingredient.name.ilike(f"%{payload.search}%"))
        result = await self.__session.execute(query)
        return result.scalars().all()

    async def get_ingredient(self, ingredient_id: int) -> Ingredient | None:
        result = await self.__session.execute(
            select(Ingredient).where(Ingredient.id == ingredient_id)
        )
        return result.scalar_one_or_none()

    async def create_ingredient(
        self, payload: IngredientCreateSchema
    ) -> Ingredient | None:
        ingredient = Ingredient(**payload.model_dump())
        self.__session.add(ingredient)
        await self.__session.commit()
        await self.__session.refresh(ingredient)
        return ingredient

    async def update_ingredient(
        self, ingredient_id: int, payload: IngredientUpdateSchema
    ) -> Ingredient | None:
        ingredient = await self.get_ingredient(ingredient_id=ingredient_id)
        if ingredient:
            ingredient.update(**payload.model_dump())
            try:
                self.__session.add(ingredient)
                await self.__session.commit()
                await self.__session.refresh(ingredient)
                return ingredient
            except IntegrityError as e:
                await self.__session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ingredient with this name already exists.",
                )
        return None

    async def delete_ingredient(self, ingredient_id: int) -> None:
        ingredient = await self.get_ingredient(ingredient_id=ingredient_id)
        if ingredient:
            await self.__session.delete(ingredient)
            await self.__session.commit()

    async def take_stock(self, ingredient_id: int, quantity: float) -> Ingredient:
        ingredient = await self.get_ingredient(ingredient_id=ingredient_id)
        if ingredient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found",
            )
        ingredient.update(quantity=ingredient.quantity - quantity)
        self.__session.add(ingredient)
        await self.__session.commit()
        await self.__session.refresh(ingredient)
        return ingredient

    async def low_stock_ingredients(self, limit, offset) -> Sequence[Ingredient]:
        query = (
            select(Ingredient)
            .offset((offset - 1) * limit)
            .limit(limit)
            .where(Ingredient.quantity <= Ingredient.min_threshold)
        )
        result = await self.__session.execute(query)
        return result.scalars().all()
