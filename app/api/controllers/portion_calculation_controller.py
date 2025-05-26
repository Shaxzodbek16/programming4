from collections.abc import Sequence

from fastapi import Depends, HTTPException, status
from math import floor

from app.api.repositories import (
    PortionCalculationRepository,
    MealRepository,
    IngredientRepository,
)
from app.api.schemas.base import QueryList
from app.api.schemas.meal_schemas import MealReadSchema, MealListQuery
from app.api.schemas.portion_calculation_schema import (
    PortionCalculationListSchema,
    PortionCalculationReadSchema,
)


class PortionCalculationController:
    def __init__(
        self,
        portion_calculation_repository: PortionCalculationRepository = Depends(),
        meal_repository: MealRepository = Depends(),
        ingredient_repository: IngredientRepository = Depends(),
    ):
        self.__portion_calculation_repository = portion_calculation_repository
        self.__meal_repository = meal_repository
        self.__ingredient_repository = ingredient_repository

    async def get_portion_count(
        self, payload: MealListQuery
    ) -> PortionCalculationListSchema:
        meals = await self.__meal_repository.list_meals(payload=payload)
        if not meals:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="There is no meal available yet.",
            )

        items = []
        for meal in meals:
            meal_ingredients = await self.__meal_repository.get_meal_ingredients(
                meal.id
            )
            possible: float = float("inf")
            for meal_ingredient in meal_ingredients:
                ingredient = await self.__ingredient_repository.get_ingredient(
                    meal_ingredient.ingredient_id
                )
                possible = min(
                    possible, ingredient.quantity / meal_ingredient.required_qty
                )

            items.append(
                PortionCalculationReadSchema(
                    meal=MealReadSchema.model_validate(meal),
                    portion_count=floor(possible),
                )
            )

        return PortionCalculationListSchema(
            search=payload.search,
            page=payload.page,
            size=payload.size,
            total=len(meals),
            items=items,
        )

    async def calculate_portions(self, meal_ingredients: Sequence | list) -> int:
        possible: float = float("inf")
        for meal_ingredient in meal_ingredients:
            ingredient = await self.__ingredient_repository.get_ingredient(
                meal_ingredient.ingredient_id
            )
            possible = min(possible, ingredient.quantity / meal_ingredient.required_qty)
        return floor(possible)

    async def get_portion_count_by_id(
        self, meal_id: int
    ) -> PortionCalculationReadSchema:
        meal = await self.__meal_repository.get_meal(meal_id)
        if meal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )
        meal_ingredients = await self.__meal_repository.get_meal_ingredients(meal_id)
        portion_count = await self.calculate_portions(meal_ingredients)

        return PortionCalculationReadSchema(
            meal=MealReadSchema.model_validate(meal), portion_count=portion_count
        )
