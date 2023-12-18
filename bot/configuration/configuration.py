import logging
from configparser import ConfigParser
from logging import Logger
from pathlib import Path
from typing import Iterator

from ..disk import File
from .section import Section

log: Logger = logging.getLogger(__name__)

class Configuration(ConfigParser, File):
    """
    A container responsible for creating and maintaining references to various
    `Section` instances.

    It is represented on disk as a configuration file.
    """

    def __init__(self, path: Path, *, exist_ok: bool = True) -> None:
        """
        Initializes a `Configuration` container.

        Args:
            path: A reference to a file on disk to be used for storing configuration data.
            exist_ok: Whether the provided file should be created on disk if it does not exist.
        """

        # initialize the parent File class
        File.__init__(self, path, exist_ok=exist_ok)
        # initialize the parent ConfigParser class
        ConfigParser.__init__(self)

        self.__read__()

    def __setitem__(self, key: str, value: Section) -> None:
        try:
            self.__read__()
            value: None = super().__setitem__(key, value)
            self.__write__()
            log.debug('SET %s:%s', self.name, key)
            return value
        except Exception:
            raise

    def __getitem__(self, key: str) -> Section:
        try:
            self.__read__()
            value: Section = super().__getitem__(key)
            self.__write__()
            log.debug('GET %s:%s', self.name, key)
            return Section.convert(value, path=self._path)
        except KeyError:
            new: Section = Section(self, key, path=self._path)
            self.__setitem__(key, new)
            self.__write__()
            return self.__getitem__(key)
            raise

    def __delitem__(self, key: str) -> None:
        try:
            self.__read__()
            value: None = super().__delitem__(key)
            self.__write__()
            log.debug('DEL %s:%s', self.name, key)
            return value
        except Exception:
            raise

    def __iter__(self) -> Iterator[str]:
        return super().__iter__()

    def __len__(self) -> int:
        return super().__len__()

    def __str__(self) -> str:
        return super().__str__()


    def __write__(self) -> None:
        """Saves data from memory to the underlying configuration file."""
        with open(self.path, 'w') as file:
            super().write(file)
        log.debug('Wrote configuration state to %s', self.name)

    def __read__(self) -> None:
        """Loads data from the underlying configuration file to memory."""
        super().read(self.path)
        log.debug('Read configuration state from %s', self.name)
