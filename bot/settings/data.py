import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from .section import SettingsSection

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
        return self.get_directory(key)
    @components.setter
    def components(self, reference: Path) -> None:
        key: str = "components"
        self[key] = str(reference)
    
    @property
    def log_config(self) -> Optional[Path]:
        key: str = "log_config"
        return self.get_file(key)
    @log_config.setter
    def log_config(self, reference: Path) -> None:
        key: str = "log_config"
        self[key] = str(reference)

    @property
    def sync(self) -> Optional[bool]:
        key: str = "sync_commands"
        return self.get_boolean(key)
    @sync.setter
    def sync(self, value: bool) -> None:
        key: str = "sync_commands"
        self[key] = str(value)

    @property
    def owner(self) -> Optional[int]:
        key: str = "owner"
        return self.get_integer(key)
    @owner.setter
    def owner(self, value: int) -> None:
        key: str = "owner"
        self[key] = str(value)
