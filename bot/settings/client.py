import logging
from logging import Logger
from pathlib import Path
from typing import cast

from ..configuration import Configuration
from .logger import LoggerSection
from .data import DataSection
from .token import TokenSection

log: Logger = logging.getLogger(__name__)

class ClientConfiguration(Configuration):
    def __init__(self, reference: Path, *, prompt: bool = False) -> None:
        super().__init__(reference)
        
        self['TOKENS'] = TokenSection(self._reference, self._parser, prompt=prompt)
        self['DATA'] = DataSection(self._reference, self._parser, prompt=prompt)
        self['LOGGING'] = LoggerSection(self._reference, self._parser, prompt=prompt)

    @property
    def token(self) -> TokenSection:
        return cast(TokenSection, self['TOKENS'])

    @property
    def data(self) -> DataSection:
        return cast(DataSection, self['DATA'])

    @property
    def logger(self) -> LoggerSection:
        return cast(LoggerSection, self['LOGGING'])
