import logging
from collections.abc import MutableMapping
from configparser import ConfigParser, DuplicateSectionError, NoOptionError
from logging import Logger
from pathlib import Path
from typing import Iterator

from ..file import File

log: Logger = logging.getLogger(__name__)

class Section(File, MutableMapping[str, str]):

    @property
    def name(self) -> str:
        """The name of the configuration section."""
        return self._name
    

    def __init__(self, name: str, reference: Path, parser: ConfigParser) -> None:
        super().__init__(reference)
        self._parser: ConfigParser = parser
        self._name: str = name

        try:
            self._parser.add_section(self._name)
            log.debug('Created configuration section %s:%s', self.path.name, self.name)
        except DuplicateSectionError:   # section already exists
            log.debug('Located configuration section %s:%s', self.path.name, self.name)
        except ValueError:              # name is 'DEFAULT'
            raise

            
    def __write__(self) -> None:
        with open(self.path, 'w') as file:
            self._parser.write(file)

    def __read__(self) -> None:
        self._parser.read(self.path)


    def __setitem__(self, key: str, value: str) -> None:
        try:
            self.__read__()
            self._parser.set(self.name, key, value)
            self.__write__()
            log.debug('Set entry %s:%s:%s', self.path.name, self.name, key)
        except:
            raise

    def __getitem__(self, key: str) -> str:
        try:
            self.__read__()
            entry: str = self._parser.get(self._name, key)
            log.debug('Get entry %s:%s:%s', self.path.name, self.name, key)
            return entry
        except NoOptionError:
            raise KeyError(key)

    def __delitem__(self, key: str) -> None:
        try:
            entry: str = self.__getitem__(key)
            self._parser.remove_option(self.name, entry)
            self.__write__()
            log.debug('Del entry %s:%s:%s', self.path.name, self.name, key)
        except:
            raise

    def __iter__(self) -> Iterator[str]:
        return iter({key: value for key, value in self._parser.items(self.name)})

    def __len__(self) -> int:
        return len({key: value for key, value in self._parser.items(self.name)})

    def __str__(self) -> str:
        return str({key: value for key, value in self._parser.items(self.name)})