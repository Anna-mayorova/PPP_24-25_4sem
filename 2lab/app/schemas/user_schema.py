from pydantic import BaseModel, validator
import re


class UserBase(BaseModel):
    email: str

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v


class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password too short")
        return v


class UserResponse(UserBase):
    id: int
    token: str = None

    class Config:
        from_attributes = True  # Исправлено с orm_mode


class TokenData(BaseModel):
    email: str | None = None
