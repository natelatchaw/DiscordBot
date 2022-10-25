import logging
from logging import Logger
from typing import Optional

from settings.section import SettingsSection

log: Logger = logging.getLogger(__name__)

class LimiterSettings(SettingsSection):

    @property
    def rate(self) -> Optional[float]:
        key: str = "rate"
        return self.get_float(key)
    @rate.setter
    def rate(self, value: float) -> None:
        key: str = "rate"
        self[key] = str(value)


    @property
    def count(self) -> Optional[int]:
        key: str = "count"
        return self.get_integer(key)
    @count.setter
    def count(self, value: int) -> None:
        key: str = "count"
        self[key] = str(value)
