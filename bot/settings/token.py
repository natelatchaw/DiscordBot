import logging
from logging import Logger
from typing import MutableMapping, Optional, cast

from .section import SettingsSection

log: Logger = logging.getLogger(__name__)

class TokenSettings(SettingsSection):
    @property
    def name(self, key: str = 'token') -> str:
        defaults: MutableMapping[str, str] = cast(MutableMapping[str, str], self._parser.defaults())
        try:
            raw_value: str = defaults[key]
            if not raw_value: raise KeyError()
            value: str = str(raw_value)
        except KeyError as error:
            defaults[key] = str()
            self.__write__()
            raise ValueError(f'{self._reference}:{self._name}:{key}: Missing token name') from error
        except Exception as error:
            raise ValueError(f'{self._reference}:{self._name}:{key}: Invalid token name') from error
        else:
            return value

    @name.setter
    def name(self, value: str, key: str = 'token') -> None:
        defaults: MutableMapping[str, str] = cast(MutableMapping[str, str], self._parser.defaults())
        defaults[key] = value

    @property
    def value(self) -> Optional[str]:
        key: str = self.name
        return self.get_string(key)
