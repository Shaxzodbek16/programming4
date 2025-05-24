from fastapi import APIRouter, Depends, status

from app.api.controllers import IngredientController

from app.api.schemas.ingredients_schemas import (
    IngredientCreateSchema,
    IngredientListQuery,
    IngredientUpdateSchema,
    IngredientListSchema,
    IngredientReadSchema,
)

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
    ingredient_controller: IngredientController = Depends(),
) -> IngredientListSchema:
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
    ingredient_controller: IngredientController = Depends(),
) -> IngredientReadSchema:
    return await ingredient_controller.get_ingredient(
        ingredient_id=ingredient_id,
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=IngredientReadSchema
)
async def create_ingredient(
    payload: IngredientCreateSchema,
    ingredient_controller: IngredientController = Depends(),
) -> IngredientReadSchema:
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
    ingredient_controller: IngredientController = Depends(),
) -> IngredientReadSchema:
    return await ingredient_controller.update_ingredient(
        ingredient_id=ingredient_id,
        payload=payload,
    )


@router.delete(
    "/{ingredient_id}/", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_ingredient(
    ingredient_id: int, ingredient_controller: IngredientController = Depends()
):
    return await ingredient_controller.delete_ingredient(
        ingredient_id=ingredient_id,
    )
