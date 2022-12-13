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
        - ValueError: If value cannot be parsed to a string
        """
        try:
            raw_value: str = self[key]
            if not raw_value: raise KeyError()
            value: str = str(raw_value)
        except KeyError as error:
            self[key] = str()
            raise ValueError(f'{self._reference}:{self._name}:{key}: Missing value') from error
        except Exception as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value') from error
        else:
            return value

    def set_string(self, key: str, value: Any) -> None:
        """
        Sets a string value for a given key.

        Raises:
        - ValueError: If value cannot be parsed to a string
        """
        try:
            self[key] = str(value)
        except Exception as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value') from error
        else:
            return

    def get_boolean(self, key: str) -> Optional[bool]:
        """
        Gets an boolean value for a given key.
        If the key does not exist, it is created and given an empty value.

        Raises:
        - ValueError: If value cannot be parsed to an boolean
        """
        positives: List[str] = ['1', 'true', 'True', 'yes', 'y']
        negatives: List[str] = ['0', 'false', 'False', 'no', 'n']
        try:
            value: bool = False
            raw_value: str = self.get_string(key)
            if not raw_value: raise ValueError()
            elif raw_value in positives: value = True
            elif raw_value in negatives: value = False
            else: raise ValueError()
        except ValueError as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value') from error
        else:
            return value

    def set_boolean(self, key: str, value: bool) -> None:
        """
        Sets an boolean value for a given key.

        Raises:
        - ValueError: If value cannot be parsed to a string
        """
        return self.set_string(key, value)


    def get_integer(self, key: str) -> int:
        """
        Gets an integer value for a given key.
        If the key does not exist, it is created and given an empty value.

        Raises:
        - ValueError: If value cannot be parsed to an integer
        """
        try:
            raw_value: str = self.get_string(key)
            value: int = int(raw_value)
        except ValueError as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value') from error
        else:
            return value

    def set_integer(self, key: str, value: int) -> None:
        """
        Sets an integer value for a given key.

        Raises:
        - ValueError: If value cannot be parsed to a string
        """
        return self.set_string(key, value)


    def get_float(self, key: str) -> float:
        """
        Gets a float value for a given key.
        If the key does not exist, it is created and given an empty value.

        Raises:
        - ValueError: If value cannot be parsed to a float
        """
        try:
            raw_value: str = self.get_string(key)
            value: float = float(raw_value)
        except ValueError as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value') from error
        else:
            return value            

    def set_float(self, key: str, value: float) -> None:
        """
        Sets a float value for a given key.

        Raises:
        - ValueError: If value cannot be parsed to a string
        """
        return self.set_string(key, value)


    def get_directory(self, key: str) -> Path:
        """
        Gets a Path value for a given key.

        Raises:
        - ValueError: If the provided value cannot be parsed as a Path
        """
        try:
            raw_value: str = self.get_string(key)
            value: Path = Path(raw_value)
            value = self.__create_directory__(value)
        except OSError as error:   
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value') from error
        else:
            return value
        
    def set_directory(self, key: str, value: Path) -> None:
        """
        Sets a string value for a given key.

        Raises:
        - ValueError: If value cannot be parsed to a string
        """
        return self.set_string(key, value)


    def get_file(self, key: str) -> Path:
        """
        Gets a Path value for a given key.

        Raises:
        - ValueError: If the provided value cannot be parsed as a Path
        """
        try:
            raw_value: str = self.get_string(key)
            value: Path = Path(raw_value)
            value = self.__create_file__(value)
        except Exception as error:   
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid value') from error
        else:
            return value

    def set_file(self, key: str, value: Path) -> None:
        """
        Sets a string value for a given key.

        Raises:
        - ValueError: If value cannot be parsed to a string
        """
        return self.set_string(key, value)


    def __create_directory__(self, value: Path) -> Path:
        try:
            directory: Path = value.resolve()
            log.debug('%s directory at %s', 'Existing' if directory.exists() else 'Creating', directory)
            if directory.exists(): return directory
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            log.warning(error)
            raise
        else:
            return directory
        
    def __create_file__(self, value: Path) -> Path:
        try:
            file: Path = value.resolve()
            log.debug('%s file at %s', 'Existing' if file.exists() else 'Creating', file)
            if file.exists(): return file
            file.touch(exist_ok=True)
        except Exception as error:
            log.warning(error)
            raise
        else:
            return file
