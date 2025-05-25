from fastapi import Depends, HTTPException, status
from app.api.repositories import MealRepository
from app.api.schemas.meal_schemas import (
    MealListSchema,
    MealReadSchema,
    MealCreateSchema,
    MealListQuery,
    MealUpdateSchema,
)


class MealController:
    def __init__(
        self,
        meal_repository: MealRepository = Depends(),
    ):
        self.__meal_repository = meal_repository

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
