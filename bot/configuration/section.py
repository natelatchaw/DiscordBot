from typing import Self
import logging
from collections.abc import MutableMapping
from configparser import ConfigParser, NoOptionError, NoSectionError, SectionProxy
from logging import Logger
from pathlib import Path
from typing import Iterator


log: Logger = logging.getLogger(__name__)

class Section(SectionProxy, MutableMapping[str, str]):

    @classmethod
    def convert(cls, section: SectionProxy, *, path: Path) -> Self:
        return cls(section._parser, section.name, path=path)
    
    def __init__(self, parser: ConfigParser, name: str, *, path: Path) -> None:
        """
        Initializes a `Section` container.

        Args:
            parser: A reference to the `Configuration` container's `ConfigParser`.
            name: The name of the section.
            path: A reference to a file on disk to be used for storing configuration data.
        """

        SectionProxy.__init__(self, parser, name)
        if not self.parser.has_section(self.name):
            self.parser.add_section(self.name)

        # create a reference to the path of the configuration file
        self._path: Path = path

    def __setitem__(self, key: str, value: str) -> None:
        try:
            self.__read__()
            value: None = super().__setitem__(key, value)
            self.__write__()
            log.debug('SET %s:%s:%s', self._path.name, self.name, key)
            return value
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
            value: None = super().__delitem__(key)
            self.__write__()
            log.debug('DEL %s:%s:%s', self._path.name, self.name, key)
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