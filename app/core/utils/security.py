from passlib.context import CryptContext
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Any
from secrets import randbelow

from app.api.repositories import UserRepository
from app.core.settings import get_settings, Settings
from app.api.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTHandler:
    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self._settings: Settings = get_settings()
        self._secret_key: str = self._settings.SECRET_KEY
        self._algorithm: str = self._settings.ALGORITHM
        self._access_exp: int = self._settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_exp: int = self._settings.REFRESH_TOKEN_EXPIRE_MINUTES
        self._user_repository = user_repository

    def _create_token(
        self, data: dict[str, Any], expires_delta: timedelta, token_type: str
    ) -> str:
        now = datetime.now(timezone.utc)
        payload = data.copy()
        payload.update({"exp": now + expires_delta, "iat": now, "type": token_type})
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_access_token(self, data: dict[str, Any]) -> str:
        return self._create_token(
            data,
            expires_delta=timedelta(minutes=self._access_exp),
            token_type="access",
        )

    def create_refresh_token(self, data: dict[str, Any]) -> str:
        return self._create_token(
            data,
            expires_delta=timedelta(minutes=self._refresh_exp),
            token_type="refresh",
        )

    def create_tokens(self, data: dict[str, Any]) -> dict[str, str]:
        access = self.create_access_token(data)
        refresh = self.create_refresh_token(data)
        return {"access_token": access, "refresh_token": refresh}

    def verify_token(self, token: str, expected_type: str = "access") -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if payload.get("type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type: {payload.get('type')}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload

    def refresh_access_token(self, refresh_token: str) -> dict[str, str]:
        payload = self.verify_token(refresh_token, expected_type="refresh")
        data = {k: v for k, v in payload.items() if k not in ("exp", "iat", "type")}
        tokens = self.create_tokens(data)
        return {"access_token": tokens["access_token"], "refresh_token": refresh_token}

    async def get_current_user(self, token: str) -> User:
        payload = self.verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = await self._user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def check_password_strength(password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in password):
            return False
        return True

    @staticmethod
    def email_is_valid(email: str) -> bool:
        import re

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def generate_otp() -> int:
        return randbelow(10**6)


jwt_handler = JWTHandler()
security = Security()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> User:
    return await jwt_handler.get_current_user(token)
