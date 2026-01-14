import logging
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional

from discord import Client, Intents
from discord.app_commands import CommandTree

from .loader import Loader
from .settings import Settings

log: Logger = logging.getLogger(__name__)


class Core(Client):

    @property
    def permissions(self) -> int:
        return self._settings.client.general.permissions

    @property
    def directory(self) -> Path:
        return self._settings.client.loader.directory


    def __init__(self, settings: Settings) -> None:
        self._settings: Settings = settings
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
        # determine whether to sync application commands
        sync: bool = self._settings.client.loader.sync
        # determine whether to reset application commands
        clear: bool = self._settings.client.loader.reset

        # initialize the command loader
        self._loader: Loader = Loader(CommandTree(self), settings=self._settings, client=self)

        if clear:
            log.info(f'Clearing application commands')
            # clear the loader's commands
            await self._loader.clear(guild=None)
        
        if True:
            # initialize args to be passed to the command loader
            args: List[Any] = [ ]
            # initialize kwargs to be passed to the command loader
            kwargs: Dict[str, Any] = { }
            log.info('Loading application commands')
            # load components from the directory
            await self._loader.load(self.directory, extension='py', loop=self.loop, *args, **kwargs)

        if sync:
            log.info(f'Syncing application commands')
            # sync the loader's commands
            await self._loader.sync(guild=None)

