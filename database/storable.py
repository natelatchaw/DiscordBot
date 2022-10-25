
from abc import abstractmethod
from sqlite3 import Row
from typing import Any, Protocol, Tuple, Type, TypeVar

from database.table import Table

TStorable = TypeVar('TStorable', bound='Storable')


class Storable(Protocol):
    
    @classmethod
    @abstractmethod
    def __table__(self) -> Table:
        raise NotImplementedError()

    @abstractmethod
    def __values__(self) -> Tuple[Any, ...]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def __from_row__(cls: Type[TStorable], row: Row) -> TStorable:
        raise NotImplementedError()
