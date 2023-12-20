import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Mapping, MutableMapping, Optional, cast

from ..configuration import Section
from .section import TypedAccess

log: logging.Logger = logging.getLogger(__name__)

class TokenSection(TypedAccess, Section):

    def __init__(self, parser: ConfigParser, *, path: Path) -> None:
        """
        """
        
        super().__init__(parser, 'TOKENS', path=path)

        # cast the defaults section to MutableMapping as it can be modified
        self.defaults: MutableMapping[str, str] = cast(MutableMapping[str, str], self.parser.defaults())

    @property
    def token_name(self, key: str = 'token') -> str:
        """
        The name of the token to use.
        """

        try:
            self.__read__()
            value: str = self.defaults[key]
            if not value: raise KeyError()
            return str(value)
        except KeyError as error:
            self.defaults[key] = str()
            self.__write__()
            raise ValueError(f'{self._path}:{self.name}:{key}: Missing token name') from error
        
    @token_name.setter
    def token_name(self, value: str, key: str = 'token') -> None:
        self.defaults[key] = value
        self.__write__()


    @property
    def value(self) -> str:
        """The token defined by the `token_name` property."""
        return self.get_string(self.token_name)
    @value.setter
    def value(self, token: str) -> None:
        self.set_string(self.token_name, token)
