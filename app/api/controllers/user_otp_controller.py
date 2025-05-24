from socket import send_fds

from fastapi import Depends, HTTPException, status

from app.api.repositories import UserOtpRepository, UserRepository


class UserOTPController:
    def __init__(
        self,
        user_otp_repository: UserOtpRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.__user_otp_repository = user_otp_repository
        self.__user_repository = user_repository

    async def check_user_exists(self, user_id: int) -> None:
        user = await self.__user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

    async def create_user_otp(self, user_id: int, otp_code: int) -> int:
        await self.check_user_exists(user_id)
        user_otp = await self.__user_otp_repository.create_user_otp(
            user_id, otp_code=otp_code
        )
        return user_otp.otp_code

    async def get_user_otp_by_user_id(self, user_id: int) -> int:
        await self.check_user_exists(user_id)
        user_otp = await self.__user_otp_repository.get_user_otp_by_user_id(user_id)
        if not user_otp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User OTP not found",
            )
        return user_otp.otp_code

    async def delete_user_otps(self, user_id: int) -> None:
        await self.check_user_exists(user_id)
        await self.__user_otp_repository.delete_user_otps(user_id=user_id)

    async def check_user_otp(self, user_id: int, otp_code: int):
        await self.check_user_exists(user_id)
        user_otp = await self.__user_otp_repository.check_user_otp(
            user_id=user_id, otp_code=otp_code
        )
        if user_otp:
            await self.__user_repository.activate_user(user_id)
        return user_otp
