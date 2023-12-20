from collections.abc import MutableMapping
import logging
from logging import Logger
from pathlib import Path
from typing import Any, List, Optional

from ..configuration import Section

log: Logger = logging.getLogger(__name__)

class TypedAccess(MutableMapping[str, str]):

    def get_string(self, key: str) -> str:
        """
        Gets a string value for a given key.
        If the key does not exist, it is created and given an empty value.

        Args:
            key: The key to retrieve a value from.

        Raises:
            ValueError: If the provided key's value is missing or empty
        """

        try:
            # get the value stored by the key
            value: str = self[key]
            # if the retrieved value is None, raise KeyError
            if not value: raise KeyError(key)
            # return the value
            return str(value)
        except KeyError as error:
            # set the value stored by the key to an empty string
            self[key] = ''
            # raise ValueError
            raise ValueError(f'{key}: Missing {error} value') from error


    def set_string(self, key: str, value: Any) -> None:
        """
        Sets a string value for a given key.

        Args:
            key: The key to store the value to.
            value: The value to store.
        """

        self[key] = str(value)


    def get_boolean(self, key: str) -> bool:
        """
        Gets an boolean value for a given key.
        If the key does not exist, it is created and given an empty value.

        Args:
            key: The key to retrieve a value from.

        Raises:
            ValueError: If the provided key's value is missing, empty or 
            cannot be parsed to an boolean
        """

        positives: List[str] = ['1', 'true', 'yes', 'y']
        negatives: List[str] = ['0', 'false', 'no', 'n']
        # get the value stored by the key and lowercase it
        value: str = self.get_string(key).lower()
        # if the value matches a positive entry, return true
        if value in positives: return True
        # if the value matches a negative entry, return false
        if value in negatives: return False
        # if the value does not match either, raise ValueError
        raise ValueError(f'{key}: Invalid value')


    def set_boolean(self, key: str, value: bool) -> None:
        """
        Sets an boolean value for a given key.

        Args:
            key: The key to store the value to.
            value: The value to store.
        """

        self.set_string(key, value)


    def get_integer(self, key: str) -> int:
        """
        Gets an `integer` value for a given key.
        If the key does not exist, it is created and given an empty value.

        Args:
            key: The key to retrieve a value from.

        Raises:
            ValueError: If the provided key's value is missing, empty or 
            cannot be parsed to an integer
        """

        value: str = self.get_string(key)
        try:
            return int(value)
        except ValueError as error:
            raise ValueError(f'{key}: {error}') from error


    def set_integer(self, key: str, value: int) -> None:
        """
        Sets an `integer` value for a given key.

        Args:
            key: The key to store the value to.
            value: The value to store.
        """

        self.set_string(key, value)


    def get_float(self, key: str) -> float:
        """
        Gets a `float` value for a given key.
        If the key does not exist, it is created and given an empty value.

        Args:
            key: The key to retrieve a value from.

        Raises:
            ValueError: If the provided key's value is missing, empty or 
            cannot be parsed to an float
        """

        value: str = self.get_string(key)
        try:
            return float(value)
        except ValueError as error:
            raise ValueError(f'{key}: {error}') from error
        

    def set_float(self, key: str, value: float) -> None:
        """
        Sets a `float` value for a given key.

        Args:
            key: The key to store the value to.
            value: The value to store.
        """

        self.set_string(key, value)


    def get_directory(self, key: str) -> Path:
        """
        Gets a `Path` value for a given key.
        If the key does not exist, it is created and given an empty value.

        Args:
            key: The key to retrieve a value from.

        Raises:
            ValueError: If the provided key's value is missing, empty or 
            invalid/inaccessible
        """
        
        value: str = self.get_string(key)
        try:
            return TypedAccess._create_directory(Path(value))
        except OSError as error:   
            raise ValueError(f'{key}: {error}') from error
        
        
    def set_directory(self, key: str, value: Path) -> None:
        """
        Sets a `Path` value for a given key.

        Args:
            key: The key to store the value to.
            value: The value to store.
        """

        self.set_string(key, value)


    def get_file(self, key: str) -> Path:
        """
        Gets a `Path` value for a given key.

        Args:
            key: The key to retrieve a value from.

        Raises:
            ValueError: If the provided key's value is missing, empty or 
            invalid/inaccessible
        """
        
        raw_value: str = self.get_string(key)
        try:
            return TypedAccess._create_file(Path(raw_value))
        except OSError as error:
            raise ValueError(f'{key}: {error}') from error


    def set_file(self, key: str, value: Path) -> None:
        """
        Sets a `Path` value for a given key.

        Args:
            key: The key to store the value to.
            value: The value to store.
        """

        self.set_string(key, value)


    @staticmethod
    def _create_directory(value: Path) -> Path:
        """
        Creates a directory at the provided Path if it does not already exist.

        Args:
            value: The `Path` value to create a directory at.
        """

        # resolve the path
        directory: Path = value.resolve()
        try:
            # create the directory
            directory.mkdir(parents=True, exist_ok=False)
            log.debug('Created directory at %s', directory)
            return directory
        except FileExistsError as error:
            log.debug('Existing directory at %s: %s', directory, error)
            return directory

    @staticmethod
    def _create_file(value: Path) -> Path:
        """
        Creates a file at the provided Path if it does not already exist.

        Args:
            value: The `Path` value to create a file at.
        """

        # resolve the path
        file: Path = value.resolve()
        try:
            # create the file's parent directory
            file.parent.mkdir(parents=True, exist_ok=True)
            # create the file
            file.touch(exist_ok=False)
            log.debug('Created file at %s', file)
            return file
        except FileExistsError as error:
            log.debug('Existing file at %s: %s', file, error)
            return file
