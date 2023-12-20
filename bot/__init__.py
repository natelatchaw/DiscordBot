from typing import List

from . import database

from .core import Core
from .settings import Settings
from .configuration import Configuration, Section
from .protocol import Component

"""
Bot

A module-based Discord bot.
"""

__version__ = '0.0.7'
__author__ = 'Nathan Latchaw'

__all__: List[str] = [
    "database",
    "configuration",

    "Core",
    "Settings",

    "Configuration",
    "Section",

    "Component"
]