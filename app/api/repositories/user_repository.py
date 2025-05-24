from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status

from app.api.models import User
from app.api.schemas.users_schemas import (
    UserCreateSchema,
    UserListQuery,
    UserUpdateSchema,
)
from app.core.databases.postgres import get_general_session


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_user_by_id(self, user_id) -> User | None:
        query = await self.__session.execute(select(User).where(User.id == user_id))
        return query.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        query = await self.__session.execute(select(User).where(User.email == email))
        return query.scalars().first()

    async def register_user(self, payload: UserCreateSchema) -> User:
        existing_user = await self.get_user_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )
        user = User(**payload.model_dump())
        self.__session.add(user)
        await self.__session.commit()
        await self.__session.refresh(user)
        return user

    async def activate_user(self, user_id: int) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user = user.activate
        self.__session.add(user)
        await self.__session.commit()
        await self.__session.refresh(user)
        return user

    async def get_all_users(self, payload: UserListQuery) -> Sequence[User]:
        query = (
            select(User).offset((payload.page - 1) * payload.size).limit(payload.size)
        )
        if payload.search:
            query = query.where(User.first_name.ilike(f"%{payload.search}%"))
        res = await self.__session.execute(query)
        return res.scalars().all()

    async def update_user(self, user_id: int, payload: UserUpdateSchema) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user.update(**payload.model_dump())
        self.__session.add(user)
        await self.__session.commit()
        await self.__session.refresh(user)
        return user
