import logging
from logging import Logger
from pathlib import Path

from .section import SettingsSection

log: Logger = logging.getLogger(__name__)

class LoggerSettings(SettingsSection):
    
    @property
    def config(self) -> Path:
        """
        Gets the path of the logging.ini file from configuration.
        See: https://docs.python.org/3/library/logging.config.html#configuration-file-format

        Raises:
        - ValueError: If logging config file path is invalid or inaccessible
        """

        return self.get_file('logging.ini')
    

    @config.setter
    def config(self, reference: Path) -> None:
        """
        Sets the path of the logging.ini file in configuration.
        See: https://docs.python.org/3/library/logging.config.html#configuration-file-format
        """

        self.set_file('logging.ini', reference)