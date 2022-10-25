import logging
from collections.abc import MutableMapping
from configparser import ConfigParser, NoOptionError
from logging import Logger
from pathlib import Path
from typing import Dict, Iterator, List, Optional


__all__: List[str] = [
    "Section"
]

log: Logger = logging.getLogger(__name__)

class Section(MutableMapping[str, str]):

    def __setitem__(self, key: str, value: str) -> None:
        try:
            self.__read__()
            self._parser.set(self._name, key, value)
            self.__write__()
            log.debug('Set entry %s:%s:%s', self._reference.name, self._name, key)
        except:
            raise

    def __getitem__(self, key: str) -> str:
        try:
            self.__read__()
            entry: str = self._parser.get(self._name, key)
            log.debug('Get entry %s:%s:%s', self._reference.name, self._name, key)
            return entry
        except NoOptionError:
            raise KeyError(key)

    def __delitem__(self, key: str) -> None:
        try:
            entry: str = self.__getitem__(key)
            self._parser.remove_option(self._name, entry)
            self.__write__()
            log.debug('Del entry %s:%s:%s', self._reference.name, self._name, key)
        except:
            raise

    def __iter__(self) -> Iterator[str]:
        return iter({key: value for key, value in self._parser.items(self._name)})

    def __len__(self) -> int:
        return len({key: value for key, value in self._parser.items(self._name)})

    def __str__(self) -> str:
        return str({key: value for key, value in self._parser.items(self._name)})

    def __write__(self) -> None:
        with open(self._reference, 'w') as file:
            self._parser.write(file)

    def __read__(self) -> None:
        self._parser.read(self._reference)

    def __init__(self, name: str, parser: ConfigParser, reference: Path) -> None:
        self._parser: ConfigParser = parser
        self._reference: Path = reference.resolve()
        self._name: str = name
        if not self._parser.has_section(self._name):
            log.debug('Missing target configuration section %s:%s', self._reference.name, self._name)
            self._parser.add_section(self._name)
            log.debug('Missing target configuration section %s:%s', self._reference.name, self._name)

    @property
    def name(self) -> str:
        """The configuration section's name."""
        return self._name
