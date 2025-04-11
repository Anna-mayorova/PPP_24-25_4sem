from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str

# (с токеном)
class UserResponse(BaseModel):
    id: int
    email: str
    token: str

    class Config:
        orm_mode = True

# /users/me (без токена)
class UserMeResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True