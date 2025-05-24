from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import UserOTP
from app.core.databases.postgres import get_general_session


class UserOtpRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_user_otp_by_user_id(self, user_id: int) -> UserOTP | None:
        query = await self.__session.execute(
            select(UserOTP).where(UserOTP.user_id == user_id)
        )
        return query.scalar_one_or_none()

    async def delete_user_otps(self, user_id: int) -> None:
        query = await self.__session.execute(
            select(UserOTP).where(UserOTP.user_id == user_id)
        )
        user_otps = query.scalars().all()
        for user_otp in user_otps:
            await self.__session.delete(user_otp)
        await self.__session.commit()

    async def create_user_otp(self, user_id: int, otp_code: int) -> UserOTP:
        await self.delete_user_otps(user_id=user_id)
        user_otp = UserOTP(user_id=user_id, otp_code=otp_code)
        self.__session.add(user_otp)
        await self.__session.commit()
        await self.__session.refresh(user_otp)
        return user_otp

    async def check_user_otp(self, user_id: int, otp_code: int) -> bool:
        user_otp = await self.get_user_otp_by_user_id(user_id)
        if not user_otp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User OTP not found",
            )
        if user_otp.otp_code != otp_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP code",
            )
        await self.delete_user_otps(user_id=user_id)
        return True
