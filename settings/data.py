import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from settings.section import SettingsSection

log: Logger = logging.getLogger(__name__)


class DataSettings(SettingsSection):
    
    @property
    def permissions(self) -> Optional[int]:
        key: str = "permissions"
        return self.get_integer(key)
    @permissions.setter
    def permissions(self, flag: int) -> None:
        key: str = "permissions"
        self[key] = str(flag)
    
    @property
    def components(self) -> Optional[Path]:
        key: str = "components"
        return self.get_path(key)
    @components.setter
    def components(self, reference: Path) -> None:
        key: str = "components"
        self[key] = str(reference)

    @property
    def owner(self) -> Optional[int]:
        key: str = "owner"
        return self.get_integer(key)
    @owner.setter
    def owner(self, value: int) -> None:
        key: str = "owner"
        self[key] = str(value)