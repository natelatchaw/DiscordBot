import logging
from pathlib import Path

from ..configuration import Configuration
from .logger import LoggerSection
from .data import DataSection
from .token import TokenSection


log: logging.Logger = logging.getLogger(__name__)

class ClientConfiguration(Configuration):
    """
    """
    
    def __init__(self, path: Path) -> None:
        """
        Args:
            path: A path referencing the configuration file to utilize.
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
