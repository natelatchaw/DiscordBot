import logging
from logging import Logger
from typing import MutableMapping, Optional

from settings.section import SettingsSection

log: Logger = logging.getLogger(__name__)

class TokenSettings(SettingsSection):
    @property
    def active(self) -> str:
        defaults: MutableMapping[str, str] = self._parser.defaults()  # type: ignore
        key: str = "token"
        value: Optional[str] = None
        try:
            value = defaults[key]
        except KeyError:
            defaults[key] = ""

        if value and isinstance(value, str):
            return value
        else:
            defaults[key] = ""
            self.__write__()
            raise ValueError(
                f"No label provided for {self._reference.name}:{self._name}:{key}"
            )

    @active.setter
    def active(self, value: str) -> None:
        key: str = "token"
        defaults: MutableMapping[str, str] = self._parser.defaults()  # type: ignore
        defaults[key] = value

    @property
    def current(self) -> Optional[str]:
        key: str = self.active
        return self.get_string(key)
