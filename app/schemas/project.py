from pydantic import BaseModel, HttpUrl

from .user import UserOut


class ProjectBase(BaseModel):
    title: str
    description: str
    url: HttpUrl


class ProjectIn(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int
    owner: UserOut

    class Config:
        orm_mode = True
