import sqlite3
from pathlib import Path
from sqlite3 import _Parameters, Connection, Row
from typing import Iterable, List, Optional, Type

from .clauses import WhereClause

from ..disk import File

from .storable import TStorable
from .table import Table

class Database(File):

    def __init__(self, reference: Path, detect_types=sqlite3.PARSE_DECLTYPES) -> None:
        # call parent initializer
        super().__init__(reference)

        # connect to the database
        self._connection: Connection = sqlite3.connect(self._path, detect_types=detect_types)
        # set the connection's row factory
        self._connection.row_factory = Row

    def create(self, type: Type[TStorable]) -> None:
        # get the table instance
        table: Table = type.__table__()
        # execute the table's create statement
        self._connection.cursor().execute(table.__create__(if_not_exists=True))
        # commit the changes
        self._connection.commit()

    def select(self, type: Type[TStorable], where: Optional[WhereClause] = None) -> Iterable[TStorable]:
        # get the table instance
        table: Table = type.__table__()
        # initialize sql parameters if a clause was provided
        parameters: _Parameters = (where._value, ) if where else ()
        # execute the table's select statement and fetch all results
        results: List[Row] = self._connection.cursor().execute(table.__select__(), parameters).fetchall()
        # initialize each result from the static class method
        return [type.__from_row__(row) for row in results]

    def insert(self, type: Type[TStorable], item: TStorable) -> None:
        # get the table instance
        table: Table = type.__table__()
        # execute the table's insert statement with parameter injection
        self._connection.cursor().execute(table.__insert__(), item.__values__())
        # commit the changes
        self._connection.commit()
