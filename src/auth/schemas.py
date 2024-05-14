from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    surname: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    password: str
    name: str
    surname: str
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserLogin(schemas.BaseUserCreate):
    email: str
    password: str







