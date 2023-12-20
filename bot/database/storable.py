from abc import abstractmethod
from sqlite3 import Row
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Type, TypeVar

from .column import Column, ColumnBuilder
from .table import Table, TableBuilder

TStorable = TypeVar('TStorable', bound='Storable')

class Storable(Protocol):
    """
    Defines a contract detailing how an implementing object should
    provide metadata to be read from and written to a SQLite database.
    """

    @property
    def _table(self) -> Table:
        """
        An implementation of this property should return a Table instance
        outlining how the class should be represented as a SQLite table.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def __table__(cls) -> Table:
        """
        An implementation of this method should return a Table instance
        outlining how the class should be represented as a SQLite table.
        """
        raise NotImplementedError()

    @abstractmethod
    def __values__(self) -> Tuple[Any, ...]:
        """
        An implementation of this method should return a Tuple of the
        instance's properties to be stored in a SQLite table row.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def __from_row__(cls: Type[TStorable], row: Row) -> TStorable:
        """
        An implementation of this method should return an instance
        of the stored object constructed from data in the row parameter.
        """
        raise NotImplementedError()



def table(*, name: str):
    def wrapper(cls: Type[Storable]) -> Type[Storable]:
        table_builder: TableBuilder = TableBuilder()
        table_builder.setName(name)

        for method_name, method in cls.__dict__.items():
            # if the method does not have attached column metadata, skip it
            if not hasattr(method, '_column_metadata'): continue
            # get the column metadata dictionary
            metadata: Dict[str, Any] = getattr(method, '_column_metadata')
            # check the type of the column metadata dictionary
            if not isinstance(metadata, Dict): raise TypeError('Column metadata was not assembled correctly.')
            
            column_builder: ColumnBuilder = ColumnBuilder()

            value: Optional[Any] = metadata.get('name')
            column_name: Optional[str] = value if value and isinstance(value, str) else None
            if not column_name: raise KeyError('_column_metadata.name')
            column_builder.setName(column_name)
            
            value: Optional[Any] = metadata.get('type')
            column_type: Optional[Any] = value if value and isinstance(value, str) else None
            if not column_type: raise KeyError('_column_metadata.type')
            column_builder.setType(column_type)

            value: Optional[Any] = metadata.get('is_primary')
            is_primary: Optional[bool] = value if value and isinstance(value, bool) else False
            column_builder.isPrimary(is_primary)

            value: Optional[Any] = metadata.get('is_unique')
            is_unique: Optional[bool] = value if value and isinstance(value, bool) else False
            column_builder.isUnique(is_unique)

            column: Column = column_builder.build()

            table_builder.addColumn(column)

        def __init__(self: Storable, *args: List[Any], **kwargs: Dict[str, Any]):
            # class the provided class' __init__
            cls.__init__(self, *args, **kwargs)
            self._table = table_builder.build()
            
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