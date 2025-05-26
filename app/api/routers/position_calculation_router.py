from fastapi import APIRouter, HTTPException, status, Depends

from app.api.models import User
from app.api.controllers import PortionCalculationController
from app.api.schemas.meal_schemas import MealListQuery
from app.core.utils.security import get_current_user
from app.api.schemas.portion_calculation_schema import (
    PortionCalculationReadSchema,
    PortionCalculationListSchema,
)

router = APIRouter(
    prefix="/portion-calculate",
    tags=["portion-calculate"],
)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=PortionCalculationListSchema
)
async def get_portion_count(
    payload: MealListQuery = Depends(),
    current_user: User = Depends(get_current_user),
    portion_calculation_controller: PortionCalculationController = Depends(),
) -> PortionCalculationListSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await portion_calculation_controller.get_portion_count(payload=payload)


@router.get(
    "/{meal_id}",
    status_code=status.HTTP_200_OK,
    response_model=PortionCalculationReadSchema,
)
async def get_portion_count_by_id(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    portion_calculation_controller: PortionCalculationController = Depends(),
) -> PortionCalculationReadSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await portion_calculation_controller.get_portion_count_by_id(
        meal_id=meal_id,
    )
