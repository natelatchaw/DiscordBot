import asyncio
import logging
import sys
from logging import Logger
from logging.config import fileConfig
from pathlib import Path
from typing import Optional

from .core import Core
from .settings import Settings

log: Logger = logging.getLogger(__name__)

async def main() -> None:
    client: Optional[Core] = None
    try:
        client = Core(configure)
        await client.start(client.token)
    except Exception as error:
        log.error(error)
    finally:
        if client: await client.close()

def configure(settings: Settings):
    log_config: Optional[Path] = None
    try:
        log_config = settings.client.data.log_config
        if log_config: fileConfig(log_config)
    except KeyError as error:
        log.warning(f'Failed to load {log_config if log_config else "log config"}: Missing entry for {error}')
    except Exception as error:
        log.warning(f'Failed to load {log_config if log_config else "log config"}: {error}.')

try:
    asyncio.run(main())
except KeyboardInterrupt:
    log.info('Bot stopped.')
    sys.exit(input('Press enter to exit...'))
except Exception as error:
    log.error(error)