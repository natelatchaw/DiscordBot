import argparse
import logging
from pathlib import Path
from typing import Optional


log: logging.Logger = logging.getLogger(__name__)

class Arguments():
    """
    A statically-typed set of arguments available to the application.
    """

    def __init__(self, parser: argparse.ArgumentParser) -> None:
        """
        Adds known arguments to the provided ArgumentParser and parses the arguments.
        """
        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('--setup', action='store_true')
        parser.add_argument('--token', required=False)
        parser.add_argument('--logging', type=Path)
        parser.add_argument('--components', type=Path)
        parser.add_argument('--permissions', type=int)
        self._arguments: argparse.Namespace = parser.parse_args()

    @property
    def token(self) -> Optional[str]:
        return self._arguments.token if self._arguments.token else None
    
    @property
    def logging(self) -> Optional[Path]:
        return self._arguments.logging if self._arguments.logging else None
    
    @property
    def permissions(self) -> Optional[int]:
        return self._arguments.permissions if self._arguments.permissions else 3276799
    
    @property
    def directory(self) -> Optional[Path]:
        return self._arguments.components if self._arguments.components else None
    

    @property
    def use_verbose(self) -> bool:
        return self._arguments.verbose if self._arguments.verbose else False
    
    @property
    def launch_setup(self) -> bool:
        return self._arguments.setup if self._arguments.setup else False