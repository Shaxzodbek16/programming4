from fastapi import Depends, APIRouter, status, HTTPException

from app.api.schemas.users_schemas import (
    UserReadSchema,
    UserListSchema,
    UserListQuery,
    UserUpdateSchema,
)
from app.api.models import User
from app.core.utils.security import get_current_user
from app.api.controllers import UserController

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
)
async def get_user_me(
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(UserController),
) -> UserReadSchema:
    return await user_controller.get_user_by_id(user_id=current_user.id)


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(UserController),
) -> UserReadSchema:
    if current_user.role_id in (1, 2, 3) or current_user.id == user_id:
        return await user_controller.get_user_by_id(user_id=user_id)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this resource.",
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=UserListSchema,
)
async def get_all_users(
    params: UserListQuery = Depends(),
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(),
) -> UserListSchema:
    if current_user.role_id in (1, 2, 3):
        return await user_controller.get_all_users(payload=params)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this resource.",
    )


@router.put(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
    summary="Update user by ID",
    description="Update user details by providing the user ID and the new data.",
)
async def update_user(
    user_id: int,
    payload: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(),
) -> UserReadSchema:
    if current_user.role_id in (1, 2) or current_user.id == user_id:
        return await user_controller.update_user(user_id=user_id, payload=payload)
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this resource.",
    )


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by ID",
    description="Delete a user by providing the user ID.",
)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(),
) -> None:
    if current_user.role_id in (1, 2) or current_user.id == user_id:
        await user_controller.delete_user(user_id=user_id)
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this resource.",
    )
