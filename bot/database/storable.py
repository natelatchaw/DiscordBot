from abc import abstractmethod
from sqlite3 import Row
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Type, TypeVar

from .table import Table, TableBuilder
from .column import Column, ColumnBuilder

TStorable = TypeVar('TStorable', bound='Storable')

class Storable(Protocol):
    # contains the Table configuration
    _table: Table

    @classmethod
    @abstractmethod
    def __table__(cls) -> Table:
        raise NotImplementedError()

    @abstractmethod
    def __values__(self) -> Tuple[Any, ...]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def __from_row__(cls: Type[TStorable], row: Row) -> TStorable:
        raise NotImplementedError()


def table(*, name: str):
    def wrapper(cls: Type[Storable]) -> Type[Storable]:
        table = TableBuilder()
        table.setName(name)

        for method_name, method in cls.__dict__.items():
            # if the method does not have attached column metadata, skip it
            if not hasattr(method, '_column_metadata'): continue
            # get the column metadata dictionary
            metadata: Dict[str, Any] = getattr(method, '_column_metadata')
            # check the type of the column metadata dictionary
            if not isinstance(metadata, Dict): raise TypeError('Column metadata was not assembled correctly.')
            
            column: ColumnBuilder = ColumnBuilder()

            value: Optional[Any] = metadata.get('name')
            column_name: Optional[str] = value if value and isinstance(value, str) else None
            if not column_name: raise KeyError('_column_metadata.name')
            column.setName(column_name)
            
            value: Optional[Any] = metadata.get('type')
            column_type: Optional[Any] = value if value and isinstance(value, str) else None
            if not column_type: raise KeyError('_column_metadata.type')
            column.setType(column_type)

            value: Optional[Any] = metadata.get('is_primary')
            is_primary: Optional[bool] = value if value and isinstance(value, bool) else False
            column.isPrimary(is_primary)

            value: Optional[Any] = metadata.get('is_unique')
            is_unique: Optional[bool] = value if value and isinstance(value, bool) else False
            column.isUnique(is_unique)

            table.addColumn(column.column())

        def __init__(self: Storable, *args: List[Any], **kwargs: Dict[str, Any]):
            # class the provided class' __init__
            cls.__init__(self, *args, **kwargs)
            self._table = table.table()
            
        # set the class __init__ to the modified init
        cls.__init__ = __init__
        # return the modified class
        return cls
    return wrapper

def column(*, name: str, type: str, is_primary: bool = False, is_unique: bool = False):
    def wrapper(func: Callable[..., Any]):
        metadata: Dict[str, Any] = {
            'name': name,
            'type': type,
            'is_primary': is_primary,
            'is_unique': is_unique
        }
        setattr(func, '_column_metadata', metadata)
        return func
    return wrapper