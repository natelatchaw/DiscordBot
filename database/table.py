from __future__ import annotations

from typing import List, Optional

from database.column import Column

class Table:

    @property
    def _fully_qualified_name(self) -> Optional[str]:
        terms: List[str] = list()
        # add the schema to the list of terms if it exists
        if self._schema: terms.append(self._schema)
        # add the name to the list of terms if it exists
        if self._name: terms.append(self._name)
        # join the terms with a period character 
        value: str = '.'.join(terms)
        return value

    def __init__(self) -> None:
        self._schema: Optional[str] = None
        self._name: Optional[str] = None
        self._columns: List[Column] = list()

    def __create__(self, *, if_not_exists: bool = True) -> str:
        """
        Get the SQL statement responsible for creating the table

        Parameters:
        - if_not_exists (bool):
            if True, includes 'IF NOT EXISTS' in the statement.
        """
        terms: List[str] = list()
        # add the create table command to the list of terms
        terms.append('CREATE TABLE')
        # add the if not exists term to the list of terms if marked
        if if_not_exists: terms.append('IF NOT EXISTS')
        # add the name to the list of terms if it exists
        if self._name: terms.append(self._fully_qualified_name)
        # join the terms with a space character
        sql: str = ' '.join(terms)
        
        # get the statement for each column
        columns: List[str] = [column.__sql__() for column in self._columns]
        # join each statement with a comma
        delimited_columns: str = ', '.join(columns)

        return f'{sql} ({delimited_columns})'

    def __select__(self) -> str:
        """
        Get the SQL statement responsible for selecting the table
        """
        terms: List[str] = list()
        # add the select command to the list of terms
        terms.append('SELECT')

        # get the statement for each column
        column_names: List[str] = [column._name for column in self._columns]
        # join each statement with a comma
        delimited_column_names: str = ', '.join(column_names)
        # add the delimited column names to the list of terms
        terms.append(delimited_column_names)

        # add the from command to the list of terms
        terms.append('FROM')
        # add the name to the list of terms if it exists
        if self._name: terms.append(self._fully_qualified_name)
        # join the terms with a space character
        sql: str = ' '.join(terms)
        
        return f'{sql}'

    def __insert__(self) -> str:
        """
        Get the SQL statement responsible for deleting the table

        Parameters:
        - if_exists (bool):
            if True, includes 'IF EXISTS' in the statement.
        """
        terms: List[str] = list()
        # add the create table command to the list of terms
        terms.append('INSERT INTO')
        # add the name to the list of terms if it exists
        if self._name: terms.append(self._fully_qualified_name)
        # join the terms with a space character
        sql: str = ' '.join(terms)
        
        # get the statement for each column
        column_names: List[str] = [column._name for column in self._columns]
        # join each statement with a comma
        delimited_column_names: str = ', '.join(column_names)
        
        # get a parameter placeholder for each column
        values: List[str] = ['?' for _ in self._columns]
        # join each statement with a comma
        delimited_values: str = ', '.join(values)

        return  f'{sql} ({delimited_column_names}) VALUES ({delimited_values})'
            
    def __delete__(self, *, if_exists: bool) -> str:
        """
        Get the SQL statement responsible for deleting the table

        Parameters:
        - if_exists (bool):
            if True, includes 'IF EXISTS' in the statement.
        """
        terms: List[str] = list()
        # add the create table command to the list of terms
        terms.append('DROP TABLE')
        # add the if exists term to the list of terms if marked
        if if_exists: terms.append('IF EXISTS')
        # add the name to the list of terms if it exists
        if self._name: terms.append(self._fully_qualified_name)
        # join the terms with a space character
        sql: str = ' '.join(terms)

        return f'{sql}'


class TableBuilder():
    
    def __init__(self) -> None:
        """
        Creates a new instance of the table builder, resetting internal state
        """
        # reset the builder state
        self.__reset__()

    def __reset__(self) -> None:
        """
        Resets the table builder's internal state
        """
        self._table: Table = Table()

    def table(self) -> Table:
        """
        Outputs the table being built and resets the builder's internal state
        """
        # get a copy of the Table instance
        table: Table = self._table
        # reset the builder state
        self.__reset__()
        # return the copied Table instance
        return table

    def setName(self, value: str) -> TableBuilder:
        """
        Sets the name of the table being built
        """
        # set the table's _name property
        self._table._name = value
        # return the builder for call chaining
        return self

    def addColumn(self, value: Column) -> TableBuilder:
        """
        Adds a column to the table being built
        """
        # add the provided column
        self._table._columns.append(value)
        # return the builder for call chaining
        return self

