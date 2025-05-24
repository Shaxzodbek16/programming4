from fastapi import APIRouter, Depends, status, HTTPException

from app.api.controllers import IngredientController
from app.api.models import User

from app.api.schemas.ingredients_schemas import (
    IngredientCreateSchema,
    IngredientListQuery,
    IngredientUpdateSchema,
    IngredientListSchema,
    IngredientReadSchema,
)
from app.core.utils.security import get_current_user

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=IngredientListSchema,
)
async def get_all_ingredients(
    params: IngredientListQuery = Depends(),
    current_user: User = Depends(get_current_user),
    ingredient_controller: IngredientController = Depends(),
) -> IngredientListSchema:
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await ingredient_controller.get_all_ingredients(
        payload=params,
    )


@router.get(
    "/{ingredient_id}",
    status_code=status.HTTP_200_OK,
    response_model=IngredientReadSchema,
)
async def get_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_user),
    ingredient_controller: IngredientController = Depends(),
) -> IngredientReadSchema:
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await ingredient_controller.get_ingredient(
        ingredient_id=ingredient_id,
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=IngredientReadSchema
)
async def create_ingredient(
    payload: IngredientCreateSchema,
    current_user: User = Depends(get_current_user),
    ingredient_controller: IngredientController = Depends(),
) -> IngredientReadSchema:
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await ingredient_controller.create_ingredient(
        payload=payload,
    )


@router.put(
    "/{ingredient_id}/",
    status_code=status.HTTP_200_OK,
    response_model=IngredientReadSchema,
)
async def update_ingredient(
    ingredient_id: int,
    payload: IngredientUpdateSchema,
    current_user: User = Depends(get_current_user),
    ingredient_controller: IngredientController = Depends(),
) -> IngredientReadSchema:
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await ingredient_controller.update_ingredient(
        ingredient_id=ingredient_id,
        payload=payload,
    )


@router.delete(
    "/{ingredient_id}/", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_user),
    ingredient_controller: IngredientController = Depends(),
):
    if current_user.role_id not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await ingredient_controller.delete_ingredient(
        ingredient_id=ingredient_id,
    )
