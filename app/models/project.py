from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .user import User


class Project(Base):
    __tablename__ = 'projects'

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    description: str = Column(String)
    url: str = Column(String)
    owner_id: int = Column(Integer, ForeignKey('users.id'))

    owner: User = relationship('User', back_populates='projects')
