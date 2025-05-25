from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.api.schemas.base import QueryList


class UserResendSchema(BaseModel):
    email: str
    model_config = ConfigDict(from_attributes=True)


class UserLoginSchema(UserResendSchema):
    password: str
    model_config = ConfigDict(from_attributes=True)


class UserBaseSchema(UserResendSchema):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    profile_picture: str | None = Field(None, max_length=100)
    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserBaseSchema):
    password: str = Field(..., min_length=8)


class UserUpdateSchema(BaseModel):
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    profile_picture: str | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=8)

    model_config = ConfigDict(from_attributes=True)


class UserReadSchema(UserBaseSchema):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    full_name: str

    model_config = ConfigDict(from_attributes=True)


class UserReadSchemaWithToken(UserReadSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenSchema(BaseModel):
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class UserListQuery(QueryList):
    model_config = ConfigDict(from_attributes=True)


class UserListSchema(BaseModel):
    total: int
    page: int
    size: int
    search: str | None = None
    items: list[UserReadSchema]

    model_config = ConfigDict(from_attributes=True)


class UserConfirmationSchema(UserResendSchema):
    otp_code: int

    model_config = ConfigDict(from_attributes=True)
