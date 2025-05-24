from fastapi import APIRouter, Depends, status
from app.api.controllers import AuthenticationController
from app.api.schemas.users_schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserConfirmationSchema,
    UserResendSchema,
    UserLoginSchema,
    UserReadSchemaWithToken,
    RefreshTokenSchema,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register/", status_code=status.HTTP_201_CREATED, response_model=UserReadSchema
)
async def register_user(
    payload: UserCreateSchema,
    auth_controller: AuthenticationController = Depends(),
):
    return await auth_controller.register_user(payload)


@router.post(
    "/otp/confirm/",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema,
)
async def confirm_otp(
    payload: UserConfirmationSchema,
    auth_controller: AuthenticationController = Depends(),
) -> UserReadSchema:
    return await auth_controller.confirm_otp(payload)


@router.post(
    "/otp/resend/",
)
async def resend_otp(
    payload: UserResendSchema,
    auth_controller: AuthenticationController = Depends(),
) -> UserReadSchema:
    return await auth_controller.resend_otp(payload)


@router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchemaWithToken,
)
async def login_user(
    payload: UserLoginSchema,
    auth_controller: AuthenticationController = Depends(),
) -> UserReadSchemaWithToken:
    return await auth_controller.login_user(payload)


@router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
)
async def refresh_token(
    payload: RefreshTokenSchema,
    auth_controller: AuthenticationController = Depends(),
):
    return await auth_controller.refresh_tokens(payload.refresh_token)
