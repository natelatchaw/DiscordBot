import logging
from logging import Logger
from pathlib import Path
from typing import cast
from discord import Guild

from configuration import Configuration
from settings.clientSettings import ClientSettings
from settings.guildSettings import GuildSettings

log: Logger = logging.getLogger(__name__)

class Settings():

    def __init__(self, directory: Path = Path('./config/')) -> None:
        # resolve the provided directory
        self._directory: Path = directory.resolve()
        # if the provided directory doesn't exist
        if not self._directory.exists(): self._directory.mkdir(parents=True, exist_ok=True)

        # initialize client settings
        self._client_settings: ClientSettings = ClientSettings(self._directory.joinpath('global.ini'))

    @property
    def client(self) -> ClientSettings:
        return self._client_settings

    def for_guild(self, guild: Guild) -> GuildSettings:
        return GuildSettings(self._directory, guild)