from __future__ import annotations

import logging
from configparser import ConfigParser, DuplicateSectionError, NoOptionError, NoSectionError, SectionProxy
from pathlib import Path
from typing import Generic, Iterator, Mapping, MutableMapping, TypeVar

from .disk import File

log: logging.Logger = logging.getLogger(__name__)

class Section(SectionProxy, MutableMapping[str, str]):
    
    def __init__(self, parser: ConfigParser, name: str, *, path: Path) -> None:
        """
        Initializes a `Section` container.

        Args:
            parser: A reference to the `Configuration` container's `ConfigParser`.
            name: The name of the section.
            path: A reference to a file on disk to be used for storing configuration data.
        """

        SectionProxy.__init__(self, parser, name)

        try:
            self.parser.add_section(self.name)
        except DuplicateSectionError:
            pass

        # create a reference to the path of the configuration file
        self._path: Path = path

    def __setitem__(self, key: str, value: str) -> None:
        try:
            self.__read__()
            super().__setitem__(key, value)
            self.__write__()
            log.debug('SET %s:%s:%s', self._path.name, self.name, key)
        except NoSectionError:
            raise
        except Exception:
            raise

    def __getitem__(self, key: str) -> str:
        try:
            self.__read__()
            value: str = super().__getitem__(key)
            self.__write__()
            log.debug('GET %s:%s:%s', self._path.name, self.name, key)
            return value
        except NoOptionError:
            raise KeyError(key)

    def __delitem__(self, key: str) -> None:
        try:
            self.__read__()
            super().__delitem__(key)
            self.__write__()
            log.debug('DEL %s:%s:%s', self._path.name, self.name, key)
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
        # open the parent configuration file
        with open(self._path, 'w') as file:
            # write the contents of the parser to file
            super().parser.write(file)
        log.debug('Wrote configuration state to %s:%s', self._path.name, self.name)

    def __read__(self) -> None:
        """Loads data from the underlying configuration file to memory."""
        # read the parent configuration file
        super().parser.read(self._path)
        log.debug('Read configuration state from %s:%s', self._path.name, self.name)


    @classmethod
    def convert(cls, section: SectionProxy, *, path: Path) -> Section:
        return cls(section.parser, section.name, path=path)


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

        # initialize the parent ConfigParser class
        super().__init__()
        # initialize the parent File class
        File.__init__(self, path, exist_ok=exist_ok)

        self.__read__()

    def __setitem__(self, key: str, value: Section) -> None:
        try:
            self.__read__()
            super().__setitem__(key, value)
            self.__write__()
            log.debug('SET %s:%s', self.name, key)
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
            super().__setitem__(key, new)
            self.__write__()
            return self.__getitem__(key)

    def __delitem__(self, key: str) -> None:
        try:
            self.__read__()
            super().__delitem__(key)
            self.__write__()
            log.debug('DEL %s:%s', self.name, key)
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