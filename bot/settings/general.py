from configparser import ConfigParser
import logging
from pathlib import Path
from typing import Optional
from ..arguments import Arguments
from ..configuration import Section
from ..settings.section import TypedAccess

log: logging.Logger = logging.getLogger(__name__)


class GeneralSection(TypedAccess, Section):
    """
    A `Section` of a `Configuration` instance containing values
    related to the general operation of the bot client.
    """

    def __init__(self, parser: ConfigParser, *, path: Path, args: Optional[Arguments] = None) -> None:
        """
        """
        self._arguments: Optional[Arguments] = args
        super().__init__(parser, 'GENERAL', path=path)

    def __setup__(self) -> None:
        """
        Prompts the user for values to apply.
        """

        # Permissions setup
        permissions: Optional[int] = None
        while not permissions:
            try:
                permissions = self.permissions
                print(f'Found existing permissions value: {self.permissions}')
                break
            except ValueError:
                permissions_value: str = input('Provide a permissions integer (or leave empty for default): ')
                permissions_value = permissions_value if permissions_value else '3276799'
                permissions = int(permissions_value)
        self.permissions = permissions

    def __check__(self) -> None:
        """
        Checks presence of required values.
        """
        log.debug(f'Found existing permissions value: {self.permissions}')
    
    @property
    def permissions(self) -> int:
        """
        Gets the permissions integer from configuration.

        Raises:
            ValueError: If permissions integer is missing or invalid
        """
        # arguments override
        if self._arguments and self._arguments.permissions:
            return self._arguments.permissions

        return self.get_integer('permissions')
    @permissions.setter
    def permissions(self, flag: int) -> None:
        """
        Sets the permissions integer in configuration.
        """
        return self.set_integer('permissions', flag)

    @property
    def owner(self) -> int:
        """
        Gets the owner's ID from configuration.

        Raises:
            ValueError: If owner ID is missing or invalid
        """
        return self.get_integer('owner')
    @owner.setter
    def owner(self, value: int) -> None:
        """
        Sets the owner's ID in configuration.
        """
        return self.set_integer('owner', value)