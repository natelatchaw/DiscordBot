import argparse
import asyncio
import logging
import platform
import socket
import sys
from configparser import ParsingError
from logging.config import fileConfig
from pathlib import Path
import traceback
from typing import Optional

import discord

from .core import Core
from .settings import Settings

log: logging.Logger = logging.getLogger(__name__)


parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="Discord Bot", description="A Discord Bot")
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--setup', action='store_true')
args: argparse.Namespace = parser.parse_args()

use_verbose: bool = args.verbose if args.verbose else False
launch_setup: bool = args.setup if args.setup else False


async def main(client: Optional[Core] = None) -> None:
    try:
        client = client if client else Core()
        await client.start(client.token)
    except Exception as error:
        log.error(error)
        raise
    finally:
        if client: await client.close()


def configure_logger(settings: Settings, recurse: bool = True) -> None:
    try:
        fileConfig(settings.client.logger.config)
    except ValueError as error:
        log.warning(error)
    except KeyError as error:
        raise Exception(f'Invalid {settings.client.logger.config.name} configuration file: missing {error} key') from error
    except ParsingError as error:
        raise Exception(f'Invalid {settings.client.logger.config.name} configuration file: {error.message}') from error
    except FileNotFoundError as exception:
        directory: Path = Path(exception.filename)
        directory.parent.mkdir(parents=True)
        if not recurse: raise 
        return configure_logger(settings=settings, recurse=False)
    
def display_metadata(settings: Settings) -> None:
    log.info(f'{platform.system()} {platform.machine()} @ {socket.gethostbyname(socket.gethostname())}')
    log.info(f'')


if __name__ == '__main__':
    if launch_setup: 
        settings: Settings = Settings(Path('./config'))
        settings.__setup__()
        sys.exit()

    try:
        settings: Settings = Settings(Path('./config'))
        settings.__check__('--setup')
        configure_logger(settings)
        client: Core = Core(settings=settings)
        log.info('Bot started.')
        log.info('Using Python v%s', platform.python_version())
        log.info('Using Discord.py v%s', discord.__version__)
        asyncio.run(main(client))
    except KeyboardInterrupt:
        log.info('Bot stopped.')
    except Exception as error:
        log.error(error)
        if use_verbose:
            traceback.print_exception(error)
    finally:
        input('Press enter to exit...')
        sys.exit()