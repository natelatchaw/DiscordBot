from configparser import ConfigParser
from pathlib import Path
from ..configuration import Section
from ..settings.section import TypedAccess


class GeneralSection(TypedAccess, Section):
    """
    A `Section` of a `Configuration` instance containing values
    related to the general operation of the bot client.
    """

    def __init__(self, parser: ConfigParser, *, path: Path) -> None:
        """
        """
        super().__init__(parser, 'GENERAL', path=path)
    
    @property
    def permissions(self) -> int:
        """
        Gets the permissions integer from configuration.

        Raises:
            ValueError: If permissions integer is missing or invalid
        """
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