from fastapi import APIRouter, Depends, HTTPException, status

from app.api.controllers import MealController
from app.api.models import User
from app.api.schemas.meal_schemas import (
    MealListSchema,
    MealReadSchema,
    MealCreateSchema,
    MealListQuery,
    MealUpdateSchema,
)
from app.core.utils.security import get_current_user

router = APIRouter(
    prefix="/meals",
    tags=["Meals"],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=MealListSchema)
async def list_meals(
    payload: MealListQuery = Depends(),
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
) -> MealListSchema:
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.list_meals(payload=payload)


@router.get("/{meal_id}", status_code=status.HTTP_200_OK, response_model=MealReadSchema)
async def get_meal(
    meal_id: int,
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
) -> MealReadSchema:
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.get_meal(meal_id=meal_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MealReadSchema)
async def create_meal(
    payload: MealCreateSchema,
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
) -> MealReadSchema:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.create_meal(payload=payload)


@router.put("/{meal_id}", status_code=status.HTTP_200_OK, response_model=MealReadSchema)
async def update_meal(
    meal_id: int,
    payload: MealUpdateSchema,
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
) -> MealReadSchema:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.update_meal(meal_id=meal_id, payload=payload)


@router.delete(
    "/{meal_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_meal(
    meal_id: int,
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
) -> None:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    await meal_controller.delete_meal(meal_id=meal_id)


# todo: Fucking endpoints for meal ingredients, serving, and logs


@router.get("{meal_id}/ingredients", status_code=status.HTTP_200_OK)
async def get_meal_ingredients():
    pass


@router.post(
    "{meal_id}/add-ingredients/{ingredient_id}/", status_code=status.HTTP_201_CREATED
)
async def add_ingredient_to_meal():
    pass


@router.delete(
    "{meal_id}/remove-ingredients/{ingredient_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_ingredient_from_meal():
    pass


@router.post(
    "{meal_id}/serve/",
    status_code=status.HTTP_201_CREATED,
)
async def serve_meal():
    pass


@router.get(
    "{meal_id}/logs",
    status_code=status.HTTP_200_OK,
)
async def log_meal():
    pass


@router.get(
    "{meal_id}/logs/{log_id}",
    status_code=status.HTTP_200_OK,
)
async def get_meal_log():
    pass


@router.put(
    "{meal_id}/logs/{log_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_meal_log():
    pass  # warning: It is only for superusers
