import logging
from logging import Logger
from pathlib import Path
from typing import cast
from discord import Guild

from configuration import Configuration

from settings.limiting import LimiterSettings
from settings.ux import UXSettings

log: Logger = logging.getLogger(__name__)


class GuildSettings(Configuration):
    def __init__(self, directory: Path, guild: Guild):
        super().__init__(directory.joinpath(str(guild.id) + '.ini'))
        self['UX'] = UXSettings('UX', self._parser, self._reference)
        self['LIMITING'] = LimiterSettings('LIMITING', self._parser, self._reference)

    @property
    def ux(self) -> UXSettings:
        return cast(UXSettings, self['UX'])

    @property
    def limiting(self) -> LimiterSettings:
        return cast(LimiterSettings, self['LIMITING'])
