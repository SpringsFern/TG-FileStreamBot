# This file is a part of FileStreamBot


from telethon import TelegramClient
from ..vars import Var

StreamBot = TelegramClient(
    session="WebStreamer",
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    flood_sleep_threshold=Var.SLEEP_THRESHOLD,
    receive_updates=not Var.NO_UPDATE
)

multi_clients = {}
work_loads = {}
