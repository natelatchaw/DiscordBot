import logging
from logging import Logger
from pathlib import Path
from typing import Callable, Optional

from discord import Guild

from .client import ClientSettings
from .guild import GuildSettings

log: Logger = logging.getLogger(__name__)

class Settings():

    def __init__(self, directory: Path = Path('./config/'), setup_hook: Optional[Callable[[ClientSettings], None]] = None) -> None:
        # resolve the provided directory
        self._directory: Path = directory.resolve()
        # if the provided directory doesn't exist
        if not self._directory.exists(): self._directory.mkdir(parents=True, exist_ok=True)

        # resolve the file path
        self._file: Path = self._directory.joinpath('client.ini').resolve()
        # get whether the file exists pre-initialization
        preexisting: bool = self._file.exists()
        # initialize client settings
        self._client_settings: ClientSettings = ClientSettings(self._file)

        # if the file was not preexisting and setup hook was provided
        if not preexisting and setup_hook:
            # call setup hook
            setup_hook(self._client_settings)

    @property
    def client(self) -> ClientSettings:
        return self._client_settings

    def for_guild(self, guild: Guild) -> GuildSettings:
        return GuildSettings(self._directory, guild)