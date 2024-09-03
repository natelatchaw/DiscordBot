import logging
from configparser import ConfigParser
import os
from pathlib import Path
from typing import Mapping, MutableMapping, Optional, cast

from ..arguments import Arguments
from ..configuration import Section
from .section import TypedAccess

log: logging.Logger = logging.getLogger(__name__)

TOKEN_ENVIRONMENT_KEY: str = 'DISCORD_TOKEN'

class TokenSection(TypedAccess, Section):
    """
    A `Section` of a `Configuration` instance containing values
    related to the token authentication of the bot client.    
    """

    def __init__(self, parser: ConfigParser, *, path: Path, args: Optional[Arguments] = None) -> None:
        """
        """
        
        self._arguments: Optional[Arguments] = args
        super().__init__(parser, 'TOKENS', path=path)

        # cast the defaults section to MutableMapping as it can be modified
        self.defaults: MutableMapping[str, str] = cast(MutableMapping[str, str], self.parser.defaults())

    def __setup__(self) -> None:
        """
        Prompts the user for values to apply.
        """

        # Token Name setup
        token_name: Optional[str] = None
        while not token_name or len(token_name) == 0:
            try:
                token_name = self.token_name
                print(f'Found existing token name: {self.token_name}')
                break
            except ValueError:
                token_name: str = input('Provide a nickname for your token: ')
        self.token_name = token_name

        # Token Value Setup
        token_value: Optional[str] = None
        while not token_value or len(token_value) == 0:
            try:
                token_value = self.value
                print(f'Found existing token value: {self.value}')
                break
            except ValueError:
                token_value: str = input('Provide your token: ')
        self.value = token_value

    def __check__(self) -> None:
        """
        Checks presence of required values.
        """
        log.debug(f'Found existing token name: {self.token_name}')
        log.debug(f'Found existing token value: {self.value}')
        

    @property
    def token_name(self, key: str = 'token') -> str:
        """
        The name of the token to use.
        """

        # arguments override
        if self._arguments and self._arguments.token:
            return "Provided via command-line arguments"

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
        """
        Gets the token defined by the `token_name` property
        from configuration.

        Raises:
            ValueError: If token value is missing or invalid
        """

        # arguments override
        if self._arguments and self._arguments.token:
            return self._arguments.token
        
        try:
            return self.get_string(self.token_name)
        except:
            # try to get the token value from the environment
            return self.get_environment_variable(TOKEN_ENVIRONMENT_KEY)
    
    @value.setter
    def value(self, token: str) -> None:
        self.set_string(self.token_name, token)
