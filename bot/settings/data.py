from configparser import ConfigParser
import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from .section import SettingsSection

log: Logger = logging.getLogger(__name__)

class DataSection(SettingsSection):

    def __init__(self, parser: ConfigParser, *, path: Path) -> None:
        """
        """
        
        super().__init__(parser, 'DATA', path=path)
        self._prompt: bool = False
    
    @property
    def permissions(self) -> int:
        """
        Gets the permissions integer from configuration.

        Raises:
        - ValueError: If permissions integer is missing or invalid
        """
        prompt: Optional[str] = 'Provide an value for the permissions integer: ' if self._prompt else None
        return self.get_integer('permissions', prompt=prompt)
    @permissions.setter
    def permissions(self, flag: int) -> None:
        """
        Sets the permissions integer in configuration.
        """
        return self.set_integer('permissions', flag)
    
    @property
    def components(self) -> Path:
        """
        Gets the path of the components directory from configuration.

        Raises:
        - ValueError: If components directory is missing or invalid
        """
        prompt: Optional[str] = 'Provide the location of the components folder: ' if self._prompt else None
        return self.get_directory('components', prompt=prompt)
    @components.setter
    def components(self, reference: Path) -> None:
        """
        Sets the path of the components directory in configuration.
        """
        return self.set_directory('components', reference)

    @property
    def sync(self) -> Optional[bool]:
        """
        Gets the command sync setting from configuration.

        Raises:
        - ValueError: If command sync boolean is missing or invalid
        """
        prompt: Optional[str] = 'Should the commands be synced with Discord? (y/n): ' if self._prompt else None
        return self.get_boolean('sync_commands', prompt=prompt)
    @sync.setter
    def sync(self, value: bool) -> None:
        """
        Sets the command sync setting in configuration.
        """
        return self.set_boolean('sync_commands', value)

    @property
    def owner(self) -> int:
        """
        Gets the owner's ID from configuration.

        Raises:
        - ValueError: If owner ID is missing or invalid
        """
        return self.get_integer('owner')
    @owner.setter
    def owner(self, value: int) -> None:
        """
        Sets the owner's ID in configuration.
        """
        return self.set_integer('owner', value)
