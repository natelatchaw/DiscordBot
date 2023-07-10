from configparser import ConfigParser
import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from .section import SettingsSection

log: Logger = logging.getLogger(__name__)

class LimiterSection(SettingsSection):

    def __init__(self, reference: Path, parser: ConfigParser = ...) -> None:
        super().__init__("LIMITING", reference, parser)

    @property
    def rate(self) -> Optional[float]:
        """
        The time duration in seconds during which to allow a specific number of commands.
        """

        key: str = "rate"
        try:
            return self.get_float(key)
        except ValueError:
            return None
        
        
    @rate.setter
    def rate(self, value: Optional[float]) -> None:
        key: str = "rate"
        if value:
            self.set_float(key, value)
        else:
            self.set_string(key, str())


    @property
    def count(self) -> Optional[int]:
        """
        The number of commands to allow within the span of a specific time duration.
        """

        key: str = "count"
        try:
            return self.get_integer(key)
        except ValueError:
            return None
        

    @count.setter
    def count(self, value: int) -> None:
        key: str = "count"
        self[key] = str(value)
