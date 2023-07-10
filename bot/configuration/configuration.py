import configparser
import logging
from collections.abc import MutableMapping
from configparser import ConfigParser
from logging import Logger
from pathlib import Path
from typing import Dict, Iterator, List, MutableMapping

from ..file import File
from .section import Section

log: Logger = logging.getLogger(__name__)

class Configuration(File, MutableMapping[str, Section]):

    def __init__(self, reference: Path) -> None:
        super().__init__(reference)
        self._parser: ConfigParser = configparser.ConfigParser()
        log.debug('Determined target configuration file %s at %s', self.name, self.parent)

        self.__read__()
        log.debug('Completed initial configuration read for %s', self.name)

        # create a list of sections from parser data
        sections: List[Section] = [Section(section, self.path, self._parser) for section in self._parser.sections()]
        # store each section by name in the dictionary
        self._sections: Dict[str, Section] = {section.name: section for section in sections}
        log.debug('Loaded %s sections for configuration file %s', len(self._sections), self.name)


    def __write__(self) -> None:
        with open(self.path, 'w') as file:
            self._parser.write(file)
        log.debug('Wrote configuration state to %s', self.name)

    def __read__(self) -> None:
        self._parser.read(self.path)
        log.debug('Read configuration state from %s', self.name)


    def __setitem__(self, key: str, value: Section) -> None:
        self.__read__()
        self._sections.__setitem__(key, value)
        self.__write__()
        log.debug('Set entry %s:%s', self.name, key)
        return

    def __getitem__(self, key: str) -> Section:
        self.__read__()
        section: Section = self._sections.__getitem__(key) # may raise KeyError
        log.debug('Get entry %s:%s', self.name, key)
        return section

    def __delitem__(self, key: str) -> None:
        section: Section = self.__getitem__(key)
        section.clear()
        self._parser.remove_section(section.name)
        self._sections.__delitem__(key)
        self.__write__()
        log.debug('Del entry %s:%s', self.name, key)
        return

    def __iter__(self) -> Iterator[str]:
        return self._sections.__iter__()

    def __len__(self) -> int:
        return self._sections.__len__()

    def __str__(self) -> str:
        return self._sections.__str__()
