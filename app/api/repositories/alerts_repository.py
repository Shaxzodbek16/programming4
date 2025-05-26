from typing import Sequence

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.databases.postgres import get_general_session
from app.api.models import Alert
from app.api.schemas.alerts_schemas import (
    AlertsQuery,
    AlertCreateSchema,
)


class AlertsRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_alerts(self, payload: AlertsQuery) -> Sequence[Alert]:
        query = (
            select(Alert).offset((payload.page - 1) * payload.size).limit(payload.size)
        )
        if payload.search:
            query = query.where(Alert.ingredient.ilike(f"%{payload.search}%"))
        if payload.is_resolved:
            query = query.filter(Alert.is_resolved == payload.is_resolved)
        res = await self.__session.execute(query)
        return res.scalars().all()

    async def get_alert_by_id(self, alert_id: int) -> Alert | None:
        res = await self.__session.execute(select(Alert).where(Alert.id == alert_id))
        return res.scalar_one_or_none()

    async def create_alert(self, payload: AlertCreateSchema) -> Alert:
        alert = Alert(**payload.model_dump())
        self.__session.add(alert)
        await self.__session.commit()
        await self.__session.refresh(alert)
        return alert

    async def delete_alert(self, alert_id: int) -> None:
        alert = await self.get_alert_by_id(alert_id=alert_id)
        if alert:
            await self.__session.delete(alert)
            await self.__session.commit()
            return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    async def resolve_alert(self, alert_id: int) -> Alert:
        alert = await self.get_alert_by_id(alert_id)
        if alert:
            alert.resolve()
            self.__session.add(alert)
            await self.__session.commit()
            await self.__session.refresh(alert)
            return alert
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found.",
        )
