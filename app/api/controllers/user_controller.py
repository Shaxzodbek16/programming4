from fastapi import Depends, HTTPException, status

from app.api.repositories.user_repository import UserRepository
from app.api.schemas.users_schemas import (
    UserReadSchema,
    UserListSchema,
    UserListQuery,
    UserUpdateSchema,
)


class UserController:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: int) -> UserReadSchema:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserReadSchema.model_validate(user.to_dict())

    async def get_all_users(self, payload: UserListQuery) -> UserListSchema:
        users = await self.user_repository.get_all_users(payload)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="There is no users yet.",
            )
        return UserListSchema(
            total=len(users),
            page=payload.page,
            size=payload.size,
            search=payload.search,
            items=[UserReadSchema.model_validate(user) for user in users],
        )

    async def update_user(
        self, user_id: int, payload: UserUpdateSchema
    ) -> UserReadSchema:
        user = await self.user_repository.update_user(user_id, payload)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserReadSchema.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        await self.user_repository.delete_user(user_id)
