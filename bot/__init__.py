from typing import List

from .core import Core
from .loader import Loader
from .configuration import Configuration
from .database import Database, Table, Statement, StatementBuilder
from .settings import Settings

"""
Bot

A module-based Discord bot.
"""

__version__ = '0.0.7'
__author__ = 'Nathan Latchaw'

__all__: List[str] = [
    "Core",

    "Loader",

    "Configuration",

    "Database",
    "Table",
    "Statement",
    "StatementBuilder",

    "Settings",
]