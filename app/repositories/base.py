from typing import Any, List, Optional, Protocol, TypeVar

from app.models.base import Base

T = TypeVar('T', bound=Base)


class Repository(Protocol):
    def add(self, obj: T) -> T:
        raise NotImplementedError()

    def list(self, skip: int, limit: int) -> List[T]:
        raise NotImplementedError()

    def filter(self, skip: int, limit: int, **kwargs: Any) -> List[T]:
        raise NotImplementedError()

    def get(self, **kwargs: Any) -> Optional[T]:
        raise NotImplementedError()

    def update(self, obj: T) -> T:
        raise NotImplementedError()

    def remove(self, obj: T) -> None:
        raise NotImplementedError()
