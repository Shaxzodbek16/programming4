from fastapi import Depends, HTTPException, status

from app.api.repositories import IngredientRepository, UnitRepository
from app.api.schemas.ingredients_schemas import (
    IngredientListQuery,
    IngredientListSchema,
    IngredientReadSchema,
    IngredientCreateSchema,
    IngredientUpdateSchema,
)


class IngredientController:
    def __init__(
        self,
        ingredient_repository: IngredientRepository = Depends(),
        unit_repository: UnitRepository = Depends(),
    ):
        self.__ingredient_repository = ingredient_repository
        self.__unit_repository = unit_repository

    async def get_all_ingredients(
        self, payload: IngredientListQuery
    ) -> IngredientListSchema:
        ingredients = await self.__ingredient_repository.get_all_ingredients(
            payload=payload,
        )
        if not ingredients:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Ingredients are not available yet",
            )
        return IngredientListSchema(
            total=len(ingredients),
            page=payload.page,
            size=payload.size,
            items=[
                IngredientReadSchema.model_validate(ingredient)
                for ingredient in ingredients
            ],
            search=payload.search,
        )

    async def get_ingredient(self, ingredient_id: int) -> IngredientReadSchema:
        ingredient = await self.__ingredient_repository.get_ingredient(
            ingredient_id=ingredient_id,
        )
        if ingredient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found",
            )
        return IngredientReadSchema.model_validate(ingredient)

    async def create_ingredient(
        self, payload: IngredientCreateSchema
    ) -> IngredientReadSchema:
        unit = await self.__unit_repository.get_unit_by_id(unit_id=payload.unit_id)
        if unit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unit not found",
            )
        exiting_ingredient = await self.__ingredient_repository.get_ingredient_by_name(
            payload.name
        )
        if exiting_ingredient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient already exists",
            )
        ingredient = await self.__ingredient_repository.create_ingredient(
            payload=payload
        )
        return IngredientReadSchema.model_validate(ingredient)

    async def update_ingredient(
        self, ingredient_id: int, payload: IngredientUpdateSchema
    ) -> IngredientReadSchema:
        unit = await self.__unit_repository.get_unit_by_id(unit_id=payload.unit_id)
        if unit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unit not found",
            )
        ingredient = await self.__ingredient_repository.update_ingredient(
            ingredient_id=ingredient_id,
            payload=payload,
        )
        if ingredient is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ingredient not updated",
            )
        return IngredientReadSchema.model_validate(ingredient)

    async def delete_ingredient(self, ingredient_id: int) -> None:
        ingredient = await self.__ingredient_repository.get_ingredient(
            ingredient_id=ingredient_id,
        )
        if ingredient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found",
            )
        await self.__ingredient_repository.delete_ingredient(
            ingredient_id=ingredient_id,
        )
