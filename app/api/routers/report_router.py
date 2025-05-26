from fastapi import APIRouter, Depends, HTTPException, status

from app.api.models import User
from app.api.schemas.report_schema import MealLogPortionStats, MealLogQueryParams
from app.api.controllers import MealController
from app.core.utils.security import get_current_user

router = APIRouter(
    prefix="/report",
    tags=["report"],
)


@router.post("/", status_code=status.HTTP_200_OK, response_model=MealLogPortionStats)
async def get_meal_log_portion_stats(
    payload: MealLogQueryParams,
    current_user: User = Depends(get_current_user),
    meal_controller: MealController = Depends(),
) -> MealLogPortionStats:
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await meal_controller.get_meal_log_portion_stats(payload=payload)
