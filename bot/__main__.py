import argparse
import asyncio
import logging
import os
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

TOKEN_VARIABLE_NAME: str = 'TOKEN'

parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="Discord Bot", description="A Discord Bot")
args: Arguments = Arguments(parser)

def get_token(environment_variable_name: str) -> str:
    token: Optional[str] = os.environ.get(environment_variable_name)
    if not isinstance(token, str):
        raise Exception(f'A Discord Developer bot token was not found for environment variable {environment_variable_name}')
    return token

def get_logging_config(args: Arguments) -> Path:
    path: Optional[Path] = args.logging
    if not isinstance(path, Path):
        raise Exception(f'A path to the logging configuration file was not provided.')
    return path


async def main(client: Core, token: str) -> None:
    try:
        await client.start(token)
    except Exception as error:
        log.error(error)
        raise
    finally:
        await client.close()


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
        log.info('Bot started.')
        log.info('Using Python v%s', platform.python_version())
        log.info('Using Discord.py v%s', discord.__version__)

        # retrieve the path of the logging config file
        logging_config: Path = get_logging_config(args)
        # configure the logger
        configure_logger(logging_config)

        # initialize the settings instance
        settings: Settings = Settings(config_path, args=args)
        # check the settings instance
        settings.__check__('--setup')

        # retrieve the token from the environment
        token: str = get_token(TOKEN_VARIABLE_NAME)
        # initialize the Core client
        client: Core = Core(settings)
        # start the main async loop
        asyncio.run(main(client, token))

    except KeyboardInterrupt:
        log.info('Bot stopped.')
    except Exception as error:
        log.error(error)
        if args.use_verbose:
            traceback.print_exception(error)
    finally:
        input('Press enter to exit...')
        sys.exit()