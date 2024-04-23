import logging
from configparser import ConfigParser
from logging import Logger
from pathlib import Path
from typing import Optional

from ..configuration import Section
from .section import TypedAccess

log: Logger = logging.getLogger(__name__)    

class LoaderSection(TypedAccess, Section):
    """
    A `Section` of a `Configuration` instance containing values
    related to the `Loader` system.
    """

    def __init__(self, parser: ConfigParser, *, path: Path) -> None:
        """
        """        
        super().__init__(parser, 'LOADER', path=path)
    
    @property
    def directory(self) -> Path:
        """
        Gets the path of the directory from configuration.

        Raises:
            ValueError: If directory is missing or invalid
        """
        return self.get_directory('directory')
    @directory.setter
    def directory(self, reference: Path) -> None:
        """
        Sets the path of the directory in configuration.
        """
        return self.set_directory('directory', reference)

    @property
    def sync(self) -> bool:
        """
        Gets the command sync setting from configuration.

        Raises:
            ValueError: If command sync boolean is missing or invalid
        """
        return self.get_boolean('sync_commands')
    @sync.setter
    def sync(self, value: bool) -> None:
        """
        Sets the command sync setting in configuration.
        """
        return self.set_boolean('sync_commands', value)

    @property
    def reset(self) -> bool:
        """
        Gets the command reset setting from configuration.

        Raises:
            ValueError: If command reset boolean is missing or invalid
        """
        return self.get_boolean('reset_commands')
    @reset.setter
    def reset(self, value: bool) -> None:
        """
        Sets the command reset setting in configuration.
        """
        return self.set_boolean('reset_commands', value)
