import logging
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

from ..arguments import Arguments
from ..configuration import Section
from .section import TypedAccess

log: logging.Logger = logging.getLogger(__name__)

class LoggerSection(TypedAccess, Section):
    """
    A `Section` of a `Configuration` instance containing values
    related to the `Logger` system.
    """

    def __init__(self, parser: ConfigParser, *, path: Path, args: Optional[Arguments] = None) -> None:
        """
        Initializes a Logger `Configuration` section.

        Args:
            parser: A reference to the parent `Configuration` instance's parser.
            path: A path referencing the configuration file to utilize.
        """
        self._arguments: Optional[Arguments] = args
        super().__init__(parser, 'LOGGING', path=path)
    
    @property
    def config(self) -> Path:
        """
        Gets the path of the logging configuration file from the current configuration file.

        Raises:
            ValueError: If logging configuration file path is missing, empty
            or invalid/inaccessible

        See: https://docs.python.org/3/library/logging.config.html#configuration-file-format
        """
        # arguments override
        if self._arguments and self._arguments.logging:
            return self._arguments.logging
        
        return self.get_file('config_ini')    

    @config.setter
    def config(self, reference: Path) -> None:
        """
        Sets the path of the logging configuration file in the current configuration file.

        See: https://docs.python.org/3/library/logging.config.html#configuration-file-format
        """

        self.set_file('config_ini', reference)