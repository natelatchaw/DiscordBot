import logging
from logging import Logger
from typing import MutableMapping, Optional, cast

from .section import SettingsSection

log: Logger = logging.getLogger(__name__)

class TokenSettings(SettingsSection):
    @property
    def name(self, key: str = 'token') -> str:
        """
        The name of the token to use.
        """

        defaults: MutableMapping[str, str] = cast(MutableMapping[str, str], self._parser.defaults())
        try:
            value: str = defaults[key]
            if not value: raise KeyError()
            return str(value)
        except KeyError as error:
            defaults[key] = str()
            self.__write__()
            raise ValueError(f'{self._reference}:{self._name}:{key}: Missing token name') from error


    @name.setter
    def name(self, value: str, key: str = 'token') -> None:
        defaults: MutableMapping[str, str] = cast(MutableMapping[str, str], self._parser.defaults())
        defaults[key] = value


    @property
    def value(self) -> str:
        """
        The value of the token defined by the `name` property.
        """

        key: str = self.name
        return self.get_string(key)
    

    @value.setter
    def value(self, token: str) -> None:
        key: str = self.name
        self.set_string(key, token)
