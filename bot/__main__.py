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

from .arguments import Arguments

from .core import Core
from .settings import Settings

log: logging.Logger = logging.getLogger(__name__)

parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="Discord Bot", description="A Discord Bot")
args: Arguments = Arguments(parser)


async def main(client: Optional[Core] = None) -> None:
    try:
        client = client if client else Core()
        await client.start(client.token)
    except Exception as error:
        log.error(error)
        raise
    finally:
        if client: await client.close()


def configure_logger(config: Path, recurse: bool = True) -> None:
    try:
        fileConfig(config)
    except ValueError as error:
        log.warning(error)
    except KeyError as error:
        raise Exception(f'Invalid {config.name} configuration file: missing {error} key') from error
    except ParsingError as error:
        raise Exception(f'Invalid {config.name} configuration file: {error.message}') from error
    except FileNotFoundError as exception:
        directory: Path = Path(exception.filename)
        directory.parent.mkdir(parents=True)
        if not recurse: raise 
        return configure_logger(config, recurse=False)
    
def display_metadata(settings: Settings) -> None:
    log.info(f'{platform.system()} {platform.machine()} @ {socket.gethostbyname(socket.gethostname())}')
    log.info(f'')


if __name__ == '__main__':
    config_path: Path = args.config
    if args.launch_setup: 
        settings: Settings = Settings(config_path, args=args)
        settings.__setup__()
        sys.exit()

    try:
        settings: Settings = Settings(config_path, args=args)
        settings.__check__('--setup')
        configure_logger(settings.client.logger.config)
        client: Core = Core(settings=settings)
        log.info('Bot started.')
        log.info('Using Python v%s', platform.python_version())
        log.info('Using Discord.py v%s', discord.__version__)
        asyncio.run(main(client))
    except KeyboardInterrupt:
        log.info('Bot stopped.')
    except Exception as error:
        log.error(error)
        if args.use_verbose:
            traceback.print_exception(error)
    finally:
        input('Press enter to exit...')
        sys.exit()