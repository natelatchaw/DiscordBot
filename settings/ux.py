import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from settings.section import SettingsSection

log: Logger = logging.getLogger(__name__)


class UXSettings(SettingsSection):

    @property
    def prefix(self) -> Optional[str]:
        key: str = "prefix"
        return self.get_string(key)
    @prefix.setter
    def prefix(self, value: str) -> None:
        key: str = "prefix"
        self[key] = value

    @property
    def verbose(self) -> bool:
        key: str = "verbose"
        value: Optional[bool] = self.get_boolean(key)
        return value if value else False
    @verbose.setter
    def verbose(self, value: bool) -> None:
        key: str = "verbose"
        self[key] = str(value)
