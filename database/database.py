
import sqlite3
from pathlib import Path
from sqlite3 import Connection, Row
from typing import List, Type

from database.storable import TStorable
from database.table import Table


class Database():

    def __init__(self, reference: Path) -> None:
        # create an absolute reference to the database
        self._database: Path = reference.absolute()
        # if the parent directory does not exist, create it
        if not self._database.parent.exists(): self._database.parent.mkdir(parents=True, exist_ok=True)
        # if the database file does not exist, create it
        if not self._database.exists(): self._database.touch(exist_ok=True)

        # connect to the database
        self._connection: Connection = sqlite3.connect(self._database)
        # set the connection's row factory
        self._connection.row_factory = Row

    def create(self, type: Type[TStorable]) -> None:
        # get the table instance
        table: Table = type.__table__()
        # execute the table's create statement
        self._connection.cursor().execute(table.__create__(if_not_exists=True))
        # commit the changes
        self._connection.commit()

    def select(self, type: Type[TStorable]) -> List[Row]:
        # get the table instance
        table: Table = type.__table__()
        # execute the table's select statement and fetch all results
        results: List[Row] = self._connection.cursor().execute(table.__select__()).fetchall()
        # return results
        return results

    def insert(self, type: TStorable) -> None:
        # get the table instance
        table: Table = type.__table__()
        # execute the table's insert statement with parameter injection
        self._connection.cursor().execute(table.__insert__(), type.__values__())
        # commit the changes
        self._connection.commit()
