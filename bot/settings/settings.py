import logging
from logging import Logger
from pathlib import Path

from ..configuration import Configuration
from ..disk import Folder
from .client import ClientConfiguration

log: Logger = logging.getLogger(__name__)

DEFAULT_DIRECTORY: Path = Path('./config/')
DEFAULT_FILENAME: str = 'client.ini'

class Settings(Folder):
    """
    A container responsible for creating and maintaining references to various
    `Configuration` instances.
    
    It is represented on disk as a directory.
    """

    def __init__(self, path: Path, *, exist_ok: bool = True) -> None:
        """
        Initializes a `Settings` container.

        Args:
            path: A reference to a directory on disk to be used for storing configuration data.
            exist_ok: Whether the provided directory should be created on disk if it does not exist.
        """

        # initialize the parent Folder class
        super().__init__(path, exist_ok=exist_ok)

    @property
    def client(self) -> ClientConfiguration:
        # create a path to the configuration file
        path: Path = self._path.joinpath(DEFAULT_FILENAME)
        # return the configuration instance
        return ClientConfiguration(path)
    
    @property
    def application(self) -> Configuration:
        # create a path to the configuration file
        path: Path = self._path.joinpath('application.ini')
        # return the configuration instance
        return Configuration(path, exist_ok=True)
    