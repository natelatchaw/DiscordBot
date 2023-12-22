import logging
from pathlib import Path

from ..configuration import Configuration
from .data import LoaderSection
from .general import GeneralSection
from .logger import LoggerSection
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
        """
        A reference to the `Token` section in 
        configuration.
        """
        return TokenSection(self, path=self._path)
    
    @property
    def general(self) -> GeneralSection:
        """
        A reference to the `General` section in 
        configuration.
        """
        return GeneralSection(self, path=self._path)

    @property
    def loader(self) -> LoaderSection:
        """
        A reference to the `Loader` section in 
        configuration.
        """
        return LoaderSection(self, path=self._path)

    @property
    def logger(self) -> LoggerSection:
        """
        A reference to the `Logger` section in 
        configuration.
        """
        return LoggerSection(self, path=self._path)
