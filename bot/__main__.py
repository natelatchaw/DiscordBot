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
print(log.name)

async def main() -> None:
    client: Optional[Core] = None
    settings: Settings = Settings()
    configure_logger(settings)
    try:
        client = Core(settings)
        await client.start(client.token)
    except Exception as error:
        log.error(error)
    finally:
        if client: await client.close()


def configure_logger(settings: Settings):
    try:
        log_config: Path = settings.client.logger.config
        if log_config: fileConfig(log_config)
    except ValueError as error:
        log.warning(error)
    except Exception as error:
        log.warning(f'Failed to load logger configuration: {error}.')

try:
    asyncio.run(main())
except KeyboardInterrupt:
    log.info('Bot stopped.')
    sys.exit(input('Press enter to exit...'))
except Exception as error:
    log.error(error)