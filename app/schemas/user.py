from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class FullUserIn(UserBase):
    password: str
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserOut(UserBase):
    id: int
    is_active: Optional[bool] = True
    is_superuser: bool = False

    class Config:
        orm_mode = True
