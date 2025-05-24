from app.api.controllers.user_otp_controller import UserOTPController
from app.api.repositories import UserRepository
from fastapi import Depends, HTTPException, status


from app.api.schemas.users_schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserConfirmationSchema,
    UserResendSchema,
    UserLoginSchema,
    UserReadSchemaWithToken,
    RefreshTokenSchema,
)
from app.core.utils.security import jwt_handler, security, JWTHandler, Security
from app.api.tasks.email import send_verification_email


class AuthenticationController:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        opt_controller: UserOTPController = Depends(),
    ):
        self.__user_repository = user_repository
        self.__user_otp_controller = opt_controller
        self.__jwt_handler: JWTHandler = jwt_handler
        self.__security: Security = security

    async def check_validation(self, payload: UserCreateSchema) -> None:
        if not self.__security.check_password_strength(payload.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is not strong enough",
            )
        if not self.__security.email_is_valid(payload.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email is not valid"
            )

    async def generate_tokens(self, payload: dict) -> dict:
        data = {k: v for k, v in payload.items() if k not in ("password", "role_id")}
        return self.__jwt_handler.create_tokens(data)

    async def refresh_tokens(self, refresh_token: str) -> dict[str, str]:
        return self.__jwt_handler.refresh_access_token(refresh_token)

    async def register_user(self, payload: UserCreateSchema) -> UserReadSchema:
        await self.check_validation(payload)
        payload.password = self.__security.hash_password(payload.password)
        res = await self.__user_repository.register_user(payload)
        code = self.__security.generate_otp()
        await self.__user_otp_controller.create_user_otp(
            res.id, self.__security.generate_otp()
        )
        send_verification_email.delay(res.email, code)
        return UserReadSchema.model_validate(res)

    async def confirm_otp(self, payload: UserConfirmationSchema) -> UserReadSchema:
        user = await self.__user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if not await self.__user_otp_controller.check_user_otp(
            user.id, payload.otp_code
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code",
            )
        return UserReadSchema.model_validate(user)

    async def resend_otp(self, payload: UserResendSchema) -> UserReadSchema:
        user = await self.__user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        code = self.__security.generate_otp()
        await self.__user_otp_controller.create_user_otp(user.id, code)
        send_verification_email.delay(user.email, code)
        return UserReadSchema.model_validate(user)

    async def login_user(self, payload: UserLoginSchema) -> UserReadSchemaWithToken:
        user = await self.__user_repository.get_user_by_email(payload.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if not self.__security.verify_password(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )
        tokens = await self.generate_tokens(user.to_dict())
        return UserReadSchemaWithToken(**user.to_dict(), **tokens)
