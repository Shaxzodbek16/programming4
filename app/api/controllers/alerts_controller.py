from fastapi import Depends, HTTPException, status

from app.api.repositories import AlertsRepository, IngredientRepository
from app.api.schemas.alerts_schemas import (
    AlertCreateSchema,
    AlertReadSchema,
    AlertsQuery,
    AlertListSchema,
)


class AlertsController:
    def __init__(
        self,
        alerts_repository: AlertsRepository = Depends(),
        ingredient_repository: IngredientRepository = Depends(),
    ):
        self.__alerts_repository = alerts_repository
        self.__ingredient_repository = ingredient_repository

    async def get_alerts(self, payload: AlertsQuery) -> AlertListSchema:
        alters = await self.__alerts_repository.get_alerts(payload=payload)
        if not alters:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="There is no alerts available yet.",
            )
        return AlertListSchema(
            total=len(alters),
            search=payload.search,
            page=payload.page,
            size=payload.size,
            items=[AlertReadSchema.model_validate(alter) for alter in alters],
        )

    async def get_alert_by_id(self, alert_id: int) -> AlertReadSchema:
        alert = await self.__alerts_repository.get_alert_by_id(alert_id=alert_id)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found.",
            )
        return AlertReadSchema.model_validate(alert)

    async def create_alert(self, payload: AlertCreateSchema) -> AlertReadSchema:
        ingredient = await self.__ingredient_repository.get_ingredient(
            ingredient_id=payload.ingredient_id
        )
        if not ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found.",
            )
        alert = await self.__alerts_repository.create_alert(payload=payload)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create alert.",
            )
        return AlertReadSchema.model_validate(alert)

    async def delete_alert(self, alert_id: int) -> None:
        alert = await self.__alerts_repository.get_alert_by_id(alert_id=alert_id)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found.",
            )
        await self.__alerts_repository.delete_alert(alert_id=alert_id)

    async def resolve_alert(self, alert_id: int) -> AlertReadSchema:
        alert = await self.__alerts_repository.resolve_alert(alert_id=alert_id)
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found.",
            )
        return AlertReadSchema.model_validate(alert)
