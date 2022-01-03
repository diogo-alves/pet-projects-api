from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str]
    is_active: Optional[bool]


class SuperuserCreate(UserCreate):
    is_superuser: bool = False


class SuperuserUpdate(UserUpdate):
    is_superuser: Optional[bool] = False


class UserOut(UserBase):
    id: int
    is_active: Optional[bool] = True
    is_superuser: bool = False

    class Config:
        orm_mode = True
