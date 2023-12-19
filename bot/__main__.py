import asyncio
import logging
import platform
import socket
import sys
from configparser import ParsingError
from logging import Logger
from logging.config import fileConfig
from pathlib import Path
import traceback
from typing import Optional

from .core import Core
from .settings import Settings

log: Logger = logging.getLogger(__name__)

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


try:
    settings: Settings = Settings(Path('./config'))
    configure_logger(settings)
    client: Core = Core(settings=settings)
    log.info('Bot started.')
    log.info('Using Python %s', platform.python_version())
    asyncio.run(main(client))
except KeyboardInterrupt:
    log.info('Bot stopped.')
except Exception as error:
    log.error(error)
    traceback.print_exception(error)
finally:
    input('Press enter to exit...')
    sys.exit()