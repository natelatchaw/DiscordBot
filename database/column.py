from __future__ import annotations

from typing import List, Optional


class Column:
    """
    An object containing metadata needed to construct a database table column
    """

    def __init__(self) -> None:
        self._name: Optional[str] = None
        self._type: Optional[str] = None
        self._is_unique: bool = False
        self._is_primary: bool = False

    def __sql__(self) -> str:
        """
        Returns a str containing the SQL
        """
        terms: List[str] = list()
        # add the name to the list of terms if it exists
        if self._name: terms.append(self._name)
        # add the type to the list of terms if it exists
        if self._type: terms.append(self._type)
        # add the unique term to the list of terms if marked as unique
        if self._is_unique: terms.append('UNIQUE')
        # add the primary term to the list of terms if marked as primary
        if self._is_unique: terms.append('PRIMARY KEY')
        # join the terms with a space character
        sql: str = ' '.join(terms)
        return sql


class ColumnBuilder():
    
    def __init__(self) -> None:
        """
        Creates a new instance of the column builder, resetting internal state
        """
        # reset the builder state
        self.__reset__()

    def __reset__(self) -> None:
        """
        Resets the column builder's internal state
        """
        self._column: Column = Column()

    def column(self) -> Column:
        """
        Outputs the column being built and resets the builder's internal state
        """
        # get a copy of the Column instance
        column: Column = self._column
        # reset the builder state
        self.__reset__()
        # return the copied Column instance
        return column

    def setName(self, value: str) -> ColumnBuilder:
        """
        Sets the name of the column being built
        """
        # set the column's _name property
        self._column._name = value
        # return the builder for call chaining
        return self

    def isUnique(self, value: bool = True) -> ColumnBuilder:
        """
        Sets whether or not the column being built should be marked as unique
        """
        # set the column's _is_unique property
        self._column._is_unique = value
        # return the builder for call chaining
        return self

    def isPrimary(self, value: bool = True) -> ColumnBuilder:
        """
        Sets whether or not the column being built should be marked as primary
        """
        # set the column's _is_primary property
        self._column._is_primary = value
        # return the builder for call chaining
        return self

    def setType(self, value: str) -> ColumnBuilder:
        """
        Sets the declared column type of the column being built
        \n
        See: https://docs.python.org/3/library/sqlite3.html#sqlite-and-python-types
        """
        # set the column's _type property
        self._column._type = value
        # return the builder for call chaining
        return self



