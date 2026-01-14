import logging
from pathlib import Path
from typing import Optional

import discord

from ..arguments import Arguments
from ..configuration import Configuration
from ..disk import Folder
from .client import ClientConfiguration


log: logging.Logger = logging.getLogger(__name__)

DEFAULT_FILENAME: str = 'client.ini'

class Settings(Folder):
    """
    A container responsible for creating and maintaining references to various
    `Configuration` instances.
    
    It is represented on disk as a directory.
    """

    def __init__(self, path: Path, *, args: Optional[Arguments] = None, exist_ok: bool = True) -> None:
        """
        Initializes a `Settings` container.

        Args:
            path: A reference to a directory on disk to be used for storing configuration data.
            exist_ok: Whether the provided directory should be created on disk if it does not exist.
        """
        self._arguments: Optional[Arguments] = args
        # initialize the parent Folder class
        super().__init__(path, exist_ok=exist_ok)

    def __setup__(self):
        """
        Prompts the user for values to apply to `Settings`.
        """
        self.client.__setup__()

    def __check__(self, setup_flag: str):
        """
        Checks presence of required `Settings` values.
        """
        try:
            self.client.__check__()
        except Exception:
            raise Exception(f"Configuration is missing required values. Run with {setup_flag} to provide these values.")

    @property
    def client(self) -> ClientConfiguration:
        """
        Retrieves a `Configuration` instance dedicated to
        client configuration options.
        """
        # create a path to the configuration file
        path: Path = self._path.joinpath(DEFAULT_FILENAME)
        # return the configuration instance
        return ClientConfiguration(path, args=self._arguments)
    
    @property
    def application(self) -> Configuration:
        """
        Retrieves a `Configuration` instance dedicated to
        application configuration options.
        """
        # create a path to the configuration file
        path: Path = self._path.joinpath('application.ini')
        # return the configuration instance
        return Configuration(path, exist_ok=True)
    
    def for_guild(self, guild: discord.Guild):
        """
        Retrieves a `Configuration` instance dedicated to
        a specific guild's configuration options.
        """
        # create a path to the configuration file
        path: Path = self._path.joinpath(f'{guild.id}.ini')
        # return the configuration instance
        return Configuration(path, exist_ok=True)
    