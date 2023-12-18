from configparser import ConfigParser
import logging
from logging import Logger
from pathlib import Path
from typing import Optional

from .section import SettingsSection

log: Logger = logging.getLogger(__name__)

class LoggerSection(SettingsSection):

    def __init__(self, parser: ConfigParser, *, path: Path) -> None:
        """
        """

        super().__init__(parser, 'LOGGING', path=path)
        self._prompt: bool = False
    
    @property
    def config(self) -> Path:
        """
        Gets the path of the logging.ini file from configuration.
        See: https://docs.python.org/3/library/logging.config.html#configuration-file-format

        Raises:
        - ValueError: If logging config file path is invalid or inaccessible
        """
        prompt: Optional[str] = 'Provide the location of the logging configuration file: ' if self._prompt else None
        return self.get_file('logging.ini', prompt=prompt)
    

    @config.setter
    def config(self, reference: Path) -> None:
        """
        Sets the path of the logging.ini file in configuration.
        See: https://docs.python.org/3/library/logging.config.html#configuration-file-format
        """

        self.set_file('logging.ini', reference)