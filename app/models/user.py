from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.security import check_password, hash_password

from .base import Base

if TYPE_CHECKING:
    # avoid circular import
    from .project import Project

    # mypy does not suports hybrid property
    # https://github.com/python/mypy/issues/4430
    hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property


class User(Base):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
    _password: str = Column('password', String)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)

    projects: List['Project'] = relationship(
        'Project', back_populates='owner', cascade='all, delete'
    )

    @hybrid_property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, new_password: str) -> None:
        self._password = hash_password(new_password)

    def verify_password(self, plain_password: str) -> bool:
        return check_password(plain_password, self.password)
