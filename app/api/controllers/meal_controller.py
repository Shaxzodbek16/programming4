from fastapi import Depends, HTTPException, status
from app.api.repositories import MealRepository, IngredientRepository
from datetime import datetime
from app.api.schemas.ingredients_schemas import (
    IngredientReadSchema,
)
from app.api.schemas.meal_schemas import (
    MealListSchema,
    MealReadSchema,
    MealCreateSchema,
    MealListQuery,
    MealUpdateSchema,
    MealReadWithIngredientSchema,
    AddIngredientToMealSchema,
    PortionQty,
    MealLogListSchema,
    MealLogReadSchema,
)
from app.api.schemas.report_schema import (
    MealLogPortionStats,
    MealLogQueryParams,
    PortionByDay,
    PortionByMonth,
    PortionByYear,
)


class MealController:
    def __init__(
        self,
        meal_repository: MealRepository = Depends(),
        ingredient_repository: IngredientRepository = Depends(),
    ):
        self.__meal_repository = meal_repository
        self.__ingredient_repository = ingredient_repository

    async def list_meals(self, payload: MealListQuery) -> MealListSchema:
        meals = await self.__meal_repository.list_meals(payload=payload)
        if not meals:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="There is no meal available yet.",
            )
        return MealListSchema(
            items=[MealReadSchema.model_validate(meal) for meal in meals],
            total=len(meals),
            page=payload.page,
            size=payload.size,
            search=payload.search,
        )

    async def get_meal(self, meal_id: int) -> MealReadSchema:
        meal = await self.__meal_repository.get_meal(meal_id=meal_id)
        if not meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )
        return MealReadSchema.model_validate(meal)

    async def create_meal(self, payload: MealCreateSchema) -> MealReadSchema:
        meal = await self.__meal_repository.create_meal(payload=payload)
        return MealReadSchema.model_validate(meal)

    async def update_meal(
        self, meal_id: int, payload: MealUpdateSchema
    ) -> MealReadSchema:
        meal = await self.__meal_repository.update_meal(
            meal_id=meal_id, payload=payload
        )
        if not meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )
        return MealReadSchema.model_validate(meal)

    async def delete_meal(self, meal_id: int) -> None:
        await self.__meal_repository.delete_meal(meal_id=meal_id)

    async def get_meal_ingredients(self, meal_id: int) -> list[IngredientReadSchema]:
        meal_ingredients = await self.__meal_repository.get_meal_ingredients(meal_id)
        if not meal_ingredients:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="There is no ingredient available yet for this meal.",
            )
        return [
            IngredientReadSchema.model_validate(
                await self.__ingredient_repository.get_ingredient(
                    meal_ingredient.ingredient_id
                )
            )
            for meal_ingredient in meal_ingredients
        ]

    async def add_ingredient_to_meal(
        self, meal_id: int, payload: AddIngredientToMealSchema
    ) -> MealReadWithIngredientSchema:
        ingredient = await self.__ingredient_repository.get_ingredient(
            payload.ingredient_id
        )
        if not ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found.",
            )
        meal = await self.__meal_repository.get_meal(meal_id)
        if not meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )
        await self.__meal_repository.add_ingredient_to_meal(
            meal_id=meal_id, payload=payload
        )

        meal_ings = await self.__meal_repository.get_meal_ingredients(meal_id)
        return MealReadWithIngredientSchema(
            **meal.to_dict(),
            ingredients=[
                IngredientReadSchema.model_validate(
                    await self.__ingredient_repository.get_ingredient(
                        meal_ing.ingredient_id
                    )
                )
                for meal_ing in meal_ings
            ],
        )

    async def remove_ingredient_from_meal(
        self, meal_id: int, ingredient_id: int
    ) -> None:
        await self.__meal_repository.remove_ingredient_from_meal(
            meal_id=meal_id, ingredient_id=ingredient_id
        )

    async def serve_meal(
        self, user_id: int, meal_id: int, payload: PortionQty
    ) -> MealReadWithIngredientSchema:
        meal = await self.__meal_repository.get_meal(meal_id)
        if not meal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )
        meal_ingredients = await self.__meal_repository.get_meal_ingredients(meal_id)
        if not meal_ingredients:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="There is no ingredient available yet for this meal.",
            )

        for meal_ingredient in meal_ingredients:
            required_amount = payload.portion_qty * meal_ingredient.required_qty
            ingredient = await self.__ingredient_repository.get_ingredient(
                meal_ingredient.ingredient_id
            )
            if required_amount > ingredient.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Not enough {ingredient.name} in stock.",
                )
        for meal_ingredient in meal_ingredients:
            required_amount = payload.portion_qty * meal_ingredient.required_qty
            await self.__ingredient_repository.take_stock(
                meal_ingredient.ingredient_id, required_amount
            )

        await self.__meal_repository.write_meal_logs(
            meal_id=meal_id, user_id=user_id, portion_qty=payload.portion_qty
        )

        return MealReadWithIngredientSchema(
            **meal.to_dict(),
            ingredients=[
                IngredientReadSchema.model_validate(
                    await self.__ingredient_repository.get_ingredient(
                        meal_ingredient.ingredient_id
                    )
                )
                for meal_ingredient in meal_ingredients
            ],
        )

    async def log_meal(self, meal_id: int, payload: MealListQuery) -> MealLogListSchema:
        meal = await self.__meal_repository.get_meal(meal_id)
        if meal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )

        meal_logs = await self.__meal_repository.log_meal(
            meal_id=meal_id,
            payload=payload,
        )

        return MealLogListSchema(
            total=len(meal_logs),
            page=payload.page,
            size=payload.size,
            search=payload.search,
            items=[
                MealLogReadSchema.model_validate(meal_log) for meal_log in meal_logs
            ],
        )

    async def get_meal_log(self, meal_id: int, log_id: int) -> MealLogReadSchema:
        meal = await self.__meal_repository.get_meal(meal_id)
        if meal is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found.",
            )

        log = await self.__meal_repository.get_log(meal_id=meal_id, log_id=log_id)
        if log is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal log not found.",
            )

        return MealLogReadSchema.model_validate(log)

    async def get_meal_log_portion_stats(
        self, payload: MealLogQueryParams
    ) -> MealLogPortionStats:

        day_portion_count, month_portion_count, year_portion_count = (
            await self.__meal_repository.get_meal_portion_by_time(
                payload.year, payload.month
            )
        )
        return MealLogPortionStats(
            daily=[
                PortionByDay(
                    date=datetime.now(),
                    total_portions=day_portion_count,
                )
            ],
            monthly=[
                PortionByMonth(
                    month=payload.month,
                    year=payload.year,
                    total_portions=month_portion_count,
                )
            ],
            yearly=[
                PortionByYear(
                    year=payload.year,
                    total_portions=year_portion_count,
                )
            ],
        )
