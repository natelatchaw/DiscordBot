import logging
from logging import Logger
from pathlib import Path
from typing import cast

from discord import Guild

from ..configuration import Configuration
from .limiting import LimiterSection
from .ux import UXSection

log: Logger = logging.getLogger(__name__)


class GuildConfiguration(Configuration):
    def __init__(self, directory: Path, guild: Guild):
        reference: Path = directory.joinpath(str(guild.id) + '.ini')
        super().__init__(reference)
        self['UX'] = UXSection(self._reference, self._parser)
        self['LIMITING'] = LimiterSection(self._reference, self._parser)

    @property
    def ux(self) -> UXSection:
        return cast(UXSection, self['UX'])

    @property
    def limiting(self) -> LimiterSection:
        return cast(LimiterSection, self['LIMITING'])
