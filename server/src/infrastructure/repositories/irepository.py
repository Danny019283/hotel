from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar("T")

class IRespository(ABC, Generic[T]):
    @abstractmethod
    def add(self, model: T) -> None:
        pass
    @abstractmethod
    def update(self, updated_model: T) -> None:
        pass
    @abstractmethod
    def get_by_id(self, id) -> T|None:
        pass
    @abstractmethod
    def get_all(self) -> T|None:
        pass
    @abstractmethod
    def delete(self, id) -> None:
        pass