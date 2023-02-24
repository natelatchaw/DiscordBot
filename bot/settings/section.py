import logging
from logging import Logger
from pathlib import Path
from typing import Any, List, Optional

from ..configuration.section import Section

log: Logger = logging.getLogger(__name__)

class SettingsSection(Section):

    def get_string(self, key: str) -> str:
        """
        Gets a string value for a given key.
        If the key does not exist, it is created and given an empty value.

        Raises:
        - ValueError: If the provided key's value is missing or empty
        """

        try:
            value: str = self[key]
            if not value: raise KeyError()
            return str(value)
        except KeyError as error:
            self[key] = str()
            raise ValueError(f'{self._reference}:{self._name}:{key}: Missing value') from error


    def set_string(self, key: str, value: Any) -> None:
        """
        Sets a string value for a given key.
        """

        self[key] = str(value)


    def get_boolean(self, key: str) -> bool:
        """
        Gets an boolean value for a given key.
        If the key does not exist, it is created and given an empty value.

        Raises:
        - ValueError: If the provided key's value cannot be parsed to an boolean
        """

        positives: List[str] = ['1', 'true', 'yes', 'y']
        negatives: List[str] = ['0', 'false', 'no', 'n']
        
        raw_value: str = self.get_string(key).lower()
        if raw_value in positives: return True
        if raw_value in negatives: return False
        raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value')


    def set_boolean(self, key: str, value: bool) -> None:
        """
        Sets an boolean value for a given key.
        """

        self.set_string(key, value)


    def get_integer(self, key: str) -> int:
        """
        Gets an integer value for a given key.
        If the key does not exist, it is created and given an empty value.

        Raises:
        - ValueError: If the provided key's value is missing, empty,
        or cannot be parsed to an integer
        """

        value: str = self.get_string(key)
        try:
            return int(value)
        except ValueError as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: {error}') from error


    def set_integer(self, key: str, value: int) -> None:
        """
        Sets an integer value for a given key.
        """

        self.set_string(key, value)


    def get_float(self, key: str) -> float:
        """
        Gets a float value for a given key.
        If the key does not exist, it is created and given an empty value.

        Raises:
        - ValueError: If the provided key's value is missing, empty,
        or cannot be parsed to an float
        """

        value: str = self.get_string(key)
        try:
            return float(value)
        except ValueError as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: {error}') from error
        

    def set_float(self, key: str, value: float) -> None:
        """
        Sets a float value for a given key.
        """
        self.set_string(key, value)


    def get_directory(self, key: str) -> Path:
        """
        Gets a Path value for a given key.

        Raises:
        - ValueError: If the provided key's Path value is invalid or inaccessible
        """
        
        value: str = self.get_string(key)
        try:
            return self.__create_directory__(Path(value))
        except OSError as error:   
            raise ValueError(f'{self._reference}:{self._name}:{key}: {error}') from error
        
        
    def set_directory(self, key: str, value: Path) -> None:
        """
        Sets a string value for a given key.
        """

        self.set_string(key, value)


    def get_file(self, key: str) -> Path:
        """
        Gets a Path value for a given key.

        Raises:
        - ValueError: If the provided key's Path value is invalid or inaccessible
        """
        
        raw_value: str = self.get_string(key)
        try:
            return self.__create_file__(Path(raw_value))
        except OSError as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: {error}') from error


    def set_file(self, key: str, value: Path) -> None:
        """
        Sets a string value for a given key.
        """

        self.set_string(key, value)


    def __create_directory__(self, value: Path, parents: bool = True) -> Path:
        """
        Creates a directory at the provided Path if it does not already exist.
        """

        directory: Path = value.resolve()
        try:
            directory.mkdir(parents=parents, exist_ok=False)
            log.debug('Created directory at %s', directory)
            return directory
        except FileExistsError as error:
            log.debug('Existing directory at %s: %s', directory, error)
            return directory


    def __create_file__(self, value: Path) -> Path:
        """
        Creates a file at the provided Path if it does not already exist.
        """

        file: Path = value.resolve()
        try:
            file.touch(exist_ok=False)
            log.debug('Created file at %s', file)
            return file
        except FileExistsError as error:
            log.debug('Existing file at %s: %s', file, error)
            return file
