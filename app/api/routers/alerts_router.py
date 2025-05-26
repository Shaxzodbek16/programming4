from fastapi import APIRouter, Depends, status, HTTPException

from app.api.controllers import AlertsController
from app.api.models import User
from app.api.schemas.alerts_schemas import (
    AlertListSchema,
    AlertsQuery,
    AlertReadSchema,
    AlertCreateSchema,
)
from app.core.utils.security import get_current_user

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=AlertListSchema)
async def get_alerts(
    payload: AlertsQuery = Depends(),
    current_user: User = Depends(get_current_user),
    alerts_controller: AlertsController = Depends(),
) -> AlertListSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await alerts_controller.get_alerts(payload=payload)


@router.get(
    "/{alert_id}", status_code=status.HTTP_200_OK, response_model=AlertReadSchema
)
async def get_alert_by_id(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    alerts_controller: AlertsController = Depends(),
) -> AlertReadSchema:
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await alerts_controller.get_alert_by_id(alert_id=alert_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AlertReadSchema)
async def create_alert(
    payload: AlertCreateSchema,
    current_user: User = Depends(get_current_user),
    alerts_controller: AlertsController = Depends(),
):
    if current_user.role_id not in (1, 2, 3, 4):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await alerts_controller.create_alert(payload=payload)


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    alerts_controller: AlertsController = Depends(),
):
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    await alerts_controller.delete_alert(alert_id=alert_id)


@router.post(
    "/{alert_id}/resolve",
    status_code=status.HTTP_200_OK,
    response_model=AlertReadSchema,
)
async def resolve_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    alerts_controller: AlertsController = Depends(),
):
    if current_user.role_id not in (1, 2):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return await alerts_controller.resolve_alert(alert_id=alert_id)
