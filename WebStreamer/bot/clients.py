# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import asyncio
import logging
from os import environ
from telethon import TelegramClient
from telethon.sessions import MemorySession
from WebStreamer.utils.util import startup
from ..vars import Var
from . import multi_clients, work_loads, StreamBot


async def initialize_clients():
    multi_clients[0] = StreamBot
    work_loads[0] = 0
    all_tokens = dict(
        (c + 1, t)
        for c, (_, t) in enumerate(
            filter(
                lambda n: n[0].startswith("MULTI_TOKEN"), sorted(environ.items())
            )
        )
    )
    if not all_tokens:
        logging.info("No additional clients found, using default client")
        return

    async def start_client(client_id, token):
        try:
            logging.info("Starting - Client %s", client_id)
            if client_id == len(all_tokens):
                await asyncio.sleep(2)
                logging.info("This will take some time, please wait...")
            client = TelegramClient(
                session=MemorySession(),
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                flood_sleep_threshold=Var.SLEEP_THRESHOLD,
                receive_updates=False
            )
            await client.start(bot_token=token)
            await startup(client)
            try:
                await client.get_input_entity(Var.BIN_CHANNEL)
            except ValueError:
                logging.error("Client - %s is not in the Bin Channel.", client_id)
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logging.error("Failed starting Client - %s Error:", client_id, exc_info=True)

    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])
    multi_clients.update(dict(clients))
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True
        logging.info("Multi-client mode enabled")
    else:
        logging.info("No additional clients were initialized, using default client")
