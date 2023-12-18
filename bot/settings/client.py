import logging
from logging import Logger
from pathlib import Path
from typing import cast

from ..configuration import Configuration
from .logger import LoggerSection
from .data import DataSection
from .token import TokenSection


log: Logger = logging.getLogger(__name__)

class ClientConfiguration(Configuration):
    def __init__(self, path: Path, *, prompt: bool = False) -> None:
        """
        Args:
            source: A path referencing the configuration file to utilize.
        """
        super().__init__(path, exist_ok=True)

    @property
    def token(self) -> TokenSection:
        return TokenSection(self, path=self._path)

    @property
    def data(self) -> DataSection:
        return DataSection(self, path=self._path)

    @property
    def logger(self) -> LoggerSection:
        return LoggerSection(self, path=self._path)
