from fastapi import APIRouter, Depends, HTTPException, status

from app.api.controllers import MealController
from app.api.models import User
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
    if current_user.role_id not in (1, 2, 3, 4):
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
    if current_user.role_id not in (1, 2, 3, 4):
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


@router.get(
    "/{meal_id}/ingredients",
    status_code=status.HTTP_200_OK,
    response_model=list[IngredientReadSchema],
)
async def get_meal_ingredients(
    meal_id: int,
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
) -> list[IngredientReadSchema]:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.get_meal_ingredients(meal_id=meal_id)


@router.post(
    "/{meal_id}/add-ingredients/",
    status_code=status.HTTP_201_CREATED,
    response_model=MealReadWithIngredientSchema,
)
async def add_ingredient_to_meal(
    meal_id: int,
    payload: AddIngredientToMealSchema,
    current_user: User = Depends(get_current_user),
    meal_controller: MealController = Depends(),
) -> MealReadWithIngredientSchema:
    if current_user.role_id not in (1, 2, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.add_ingredient_to_meal(
        meal_id=meal_id, payload=payload
    )


@router.delete(
    "/{meal_id}/remove-ingredients/{ingredient_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def remove_ingredient_from_meal(
    meal_id: int,
    ingredient_id: int,
    current_user: User = Depends(get_current_user),
    meal_controller: MealController = Depends(),
) -> None:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.remove_ingredient_from_meal(
        meal_id=meal_id,
        ingredient_id=ingredient_id,
    )


@router.post(
    "/{meal_id}/serve/",
    status_code=status.HTTP_201_CREATED,
    response_model=MealReadWithIngredientSchema,
)
async def serve_meal(
    meal_id: int,
    payload: PortionQty,
    current_user: User = Depends(get_current_user),
    meal_controller: MealController = Depends(),
) -> MealReadWithIngredientSchema:
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.serve_meal(
        user_id=current_user.id, meal_id=meal_id, payload=payload
    )


@router.get(
    "/{meal_id}/logs", status_code=status.HTTP_200_OK, response_model=MealLogListSchema
)
async def log_meal(
    meal_id: int,
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
    payload: MealListQuery = Depends(),
) -> MealLogListSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )

    return await meal_controller.log_meal(
        meal_id=meal_id,
        payload=payload,
    )


@router.get(
    "/{meal_id}/logs/{log_id}",
    status_code=status.HTTP_200_OK,
    response_model=MealLogReadSchema,
)
async def get_meal_log(
    meal_id: int,
    log_id: int,
    meal_controller: MealController = Depends(),
    current_user: User = Depends(get_current_user),
) -> MealLogReadSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.get_meal_log(meal_id=meal_id, log_id=log_id)
