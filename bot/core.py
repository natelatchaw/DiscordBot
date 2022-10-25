import logging
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional

from discord import Client, Intents
from discord.app_commands import CommandTree

from bot.loader import Loader
from bot.settings import Settings

log: Logger = logging.getLogger(__name__)


class Core(Client):

    @property
    def permissions(self) -> int:
        permissions: Optional[int] = self._settings.client.data.permissions
        if permissions is None:
            raise ValueError('No permissions value provided.')
        return permissions

    @property
    def token(self) -> str:
        token: Optional[str] = self._settings.client.token.current
        if not token:
            raise ValueError('No token value provided.')
        return token

    @property
    def components(self) -> Path:
        components: Optional[Path] = self._settings.client.data.components
        if not components:
            raise ValueError('No components directory provided.')
        return components


    def __init__(self) -> None:
        self._settings: Settings = Settings()
        super().__init__(intents=Intents(self.permissions))


    async def on_ready(self):
        # call load hook
        await self.__load__()
        # log ready status
        log.info("Ready!")


    async def __load__(self) -> None:
        """
        Calls necessary logic for loading application commands
        """
        # initialize the command loader
        self._loader: Loader = Loader(CommandTree(self))

        # initialize args to be passed to the command loader
        args: List[Any] = [

        ]
        # initialize kwargs to be passed to the command loader
        kwargs: Dict[str, Any] = {
            'settings': self._settings
        }
        log.info('Loading application commands')
        # load components from the directory
        await self._loader.load(self.components, loop=self.loop, *args, **kwargs)
        log.info('Syncing application commands')
        # sync the loader's commands
        await self._loader.sync(guild=None)

