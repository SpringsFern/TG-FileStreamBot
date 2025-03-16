# This file is a part of TG-FileStreamBot

import asyncio
import logging
import traceback
import aiohttp
from WebStreamer.vars import Var


async def ping_server():
    sleep_time = Var.PING_INTERVAL
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(Var.URL) as resp:
                    logging.info("Pinged server with response: %s",resp.status)
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()
