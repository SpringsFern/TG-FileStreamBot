# This file is a part of TG-FileStreamBot


from telethon import TelegramClient
from ..vars import Var

StreamBot = TelegramClient(
    session="WebStreamer",
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    flood_sleep_threshold=Var.SLEEP_THRESHOLD,
    receive_updates=not Var.NO_UPDATE
)

class BotInfo():
    fname: str = None
    username: str = None

multi_clients = {}
work_loads = {}
