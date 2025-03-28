# This file is a part of TG-FileStreamBot

import logging
from telethon import Button, errors
from telethon.events import NewMessage
from telethon.extensions import html
from WebStreamer.bot import StreamBot
from WebStreamer.utils.file_properties import get_file_info, pack_file, get_short_hash
from WebStreamer.vars import Var

@StreamBot.on(NewMessage(func=lambda e: True if e.message.file and e.is_private else False))
async def media_receive_handler(event: NewMessage.Event):
    user = await event.get_sender()
    if Var.ALLOWED_USERS and not ((str(user.id) in Var.ALLOWED_USERS) or (user.username in Var.ALLOWED_USERS)):
        return await event.message.reply(
            message="You are not in the allowed list of users who can use me.",
            link_preview=False,
            parse_mode=html
        )
    try:
        log_msg=await event.message.forward_to(Var.BIN_CHANNEL)
        file_info=get_file_info(log_msg)
        full_hash = pack_file(
            file_info.file_name,
            file_info.file_size,
            file_info.mime_type,
            file_info.id
        )
        file_hash=get_short_hash(full_hash)
        stream_link = f"{Var.URL}stream/{log_msg.id}?hash={file_hash}"

        await event.message.reply(
            message=f"<code>{stream_link}</code>",
            link_preview=False,
            buttons=[
            [Button.url("Open", url=stream_link)]
            ],
            parse_mode=html
        )
    except errors.FloodWaitError as e:
        logging.error(e)
