import logging
from logging import Logger
from pathlib import Path
from typing import cast

from configuration import Configuration
from settings.data import DataSettings
from settings.token import TokenSettings

log: Logger = logging.getLogger(__name__)


class ClientSettings(Configuration):
    def __init__(self, reference: Path = Path('./config.ini')) -> None:
        super().__init__(reference)
        self['TOKENS'] = TokenSettings('TOKENS', self._parser, self._reference)
        self['DATA'] = DataSettings('DATA', self._parser, self._reference)

    @property
    def data(self) -> DataSettings:
        return cast(DataSettings, self['DATA'])

    @property
    def token(self) -> TokenSettings:
        return cast(TokenSettings, self['TOKENS'])