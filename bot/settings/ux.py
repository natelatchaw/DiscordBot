import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from .section import TypedAccess

log: logging.Logger = logging.getLogger(__name__)


class UXSection(TypedAccess):

    def __init__(self, reference: Path, parser: ConfigParser = ...) -> None:
        super().__init__('UX', reference, parser)

    @property
    def prefix(self) -> Optional[str]:
        key: str = 'prefix'
        return self.get_string(key)
    @prefix.setter
    def prefix(self, value: str) -> None:
        key: str = 'prefix'
        self[key] = value

    @property
    def verbose(self) -> bool:
        key: str = 'verbose'
        value: Optional[bool] = self.get_boolean(key)
        return value if value else False
    @verbose.setter
    def verbose(self, value: bool) -> None:
        key: str = 'verbose'
        self[key] = str(value)
