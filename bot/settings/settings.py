import logging
from logging import Logger
from pathlib import Path
from typing import Callable, Optional

from discord import Guild

from .client import ClientConfiguration
from .guild import GuildConfiguration

log: Logger = logging.getLogger(__name__)

DEFAULT_DIR: Path = Path('./config/')

class Settings():

    def __init__(self, directory: Path = DEFAULT_DIR, setup_hook: Optional[Callable[[ClientConfiguration], None]] = None) -> None:
        # resolve the provided directory
        self._directory: Path = directory.resolve()
        # create the file path
        self._file: Path = self._directory.joinpath('client.ini')
        # determine whether the file already exists
        preexisting: bool = self._file.exists()

        # initialize client settings
        self._client_settings: ClientConfiguration = ClientConfiguration(self._file)
        # if the file was not preexisting and setup hook was provided
        if not preexisting and setup_hook:
            # call setup hook
            setup_hook(self._client_settings)

    @property
    def client(self) -> ClientConfiguration:
        return self._client_settings

    def for_guild(self, guild: Guild) -> GuildConfiguration:
        return GuildConfiguration(self._directory, guild)