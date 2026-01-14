import argparse
import logging
from pathlib import Path
from typing import Optional

from ..arguments import Arguments
from ..configuration import Configuration
from .data import LoaderSection
from .general import GeneralSection

log: logging.Logger = logging.getLogger(__name__)

class ClientConfiguration(Configuration):
    """
    """
    
    def __init__(self, path: Path, *, args: Optional[Arguments] = None) -> None:
        """
        Args:
            path: A path referencing the configuration file to utilize.
        """
        self._arguments: Optional[Arguments] = args
        super().__init__(path, exist_ok=True)

    def __setup__(self):
        """
        Prompts the user for values to apply.
        """
        self.general.__setup__()
        self.loader.__setup__()

    def __check__(self):
        """
        Checks presence of required values.
        """
        self.general.__check__()
        self.loader.__check__()
    
    @property
    def general(self) -> GeneralSection:
        """
        A reference to the `General` section in 
        configuration.
        """
        return GeneralSection(self, path=self._path, args=self._arguments)

    @property
    def loader(self) -> LoaderSection:
        """
        A reference to the `Loader` section in 
        configuration.
        """
        return LoaderSection(self, path=self._path, args=self._arguments)