from pydantic import BaseModel
from pydantic.config import ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    token: str
    model_config = ConfigDict(from_attributes=True)

# /users/me (без токена)
class UserMeResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True