import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from configuration import Configuration
from configuration.section import Section

log: Logger = logging.getLogger(__name__)


class SettingsSection(Section):

    def get_boolean(self, key: str) -> Optional[bool]:
        raw_value: Optional[str] = None
        try:
            raw_value = self[key]
        except KeyError:
            self[key] = ''
        if not raw_value:
            return None
        elif not isinstance(raw_value, str):
            return None
        else:
            return raw_value.lower() == str(True).lower()

    def get_integer(self, key: str) -> Optional[int]:
        raw_value: Optional[str] = None
        try:
            raw_value = self[key]
        except KeyError:
            self[key] = ''
        if not raw_value:
            return None
        elif not isinstance(raw_value, str):
            return None
        else:
            return int(raw_value)

    def get_float(self, key: str) -> Optional[float]:
        raw_value: Optional[str] = None
        try:
            raw_value = self[key]
        except KeyError:
            self[key] = ''
        if not raw_value:
            return None
        elif not isinstance(raw_value, str):
            return None
        else:
            return float(raw_value)

    def get_string(self, key: str) -> Optional[str]:
        raw_value: Optional[str] = None
        try:
            raw_value = self[key]
        except KeyError:
            self[key] = ''
        if not raw_value:
            return None
        elif not isinstance(raw_value, str):
            return None
        else:
            return raw_value

    def get_path(self, key: str) -> Optional[Path]:
        raw_value: Optional[str] = None
        try:
            raw_value = self[key]
        except KeyError:
            self[key] = ''
        if not raw_value:
            return None
        elif not isinstance(raw_value, str):
            return None
        else:
            return self.__create_directory__(key, raw_value)

        
    def __create_directory__(self, key: str, value: str) -> Path:
        directory: Path = Path(value).resolve()
        if not directory.exists():
            log.debug("Starting %s directory creation at %s", key, directory)
            directory.mkdir(parents=True, exist_ok=True)
            return directory
        else:
            log.debug("Existing %s directory found at %s", key, directory)
            return directory
