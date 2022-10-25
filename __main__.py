import asyncio
import logging
import sys
from logging import FileHandler, Formatter, Logger, StreamHandler
from typing import Optional

import discord
import configuration

import core
from core import Core

root: Logger = logging.getLogger()

formatter: Formatter = Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s')
# formatter: Formatter = Formatter('[%(asctime)s] [%(pathname)s:%(lineno)d] [%(name)s] [%(levelname)s] %(message)s')
# formatter: Formatter = Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

stdoutHandler: StreamHandler = StreamHandler(sys.stdout)
stdoutHandler.setFormatter(formatter)
stdoutHandler.setLevel(logging.INFO)
root.addHandler(stdoutHandler)

fileHandler: FileHandler = FileHandler("./.log", encoding="utf-8")
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.DEBUG)
root.addHandler(fileHandler)

logging.addLevelName(logging.DEBUG, "DBG")
logging.addLevelName(logging.INFO, "INF")
logging.addLevelName(logging.WARN, "WRN")
logging.addLevelName(logging.ERROR, "ERR")
logging.addLevelName(logging.FATAL, "FTL")

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger(discord.__name__).setLevel(logging.WARNING)
logging.getLogger(core.__name__).setLevel(logging.DEBUG)
logging.getLogger(configuration.__name__).setLevel(logging.INFO)

log: Logger = logging.getLogger(__name__)


async def main() -> None:
    
    client: Optional[Core] = None

    try:
        client = Core()
        await client.start(client.token)
    except Exception as error:
        log.error(error)
    finally:
        if client: await client.close()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    log.info('Bot stopped.')
except Exception as error:
    log.error(error)
finally:
    sys.exit(input('Press enter to exit...'))
