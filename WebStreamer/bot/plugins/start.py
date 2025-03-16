# This file is a part of TG-FileStreamBot

from telethon.extensions import html
from telethon.events import NewMessage
from WebStreamer import __version__
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var

@StreamBot.on(NewMessage(incoming=True,pattern=r"^\/start*", func=lambda e: e.is_private))
async def start(event: NewMessage.Event):
    user = await event.get_sender()
    if Var.ALLOWED_USERS and not ((str(user.id) in Var.ALLOWED_USERS) or (user.username in Var.ALLOWED_USERS)):
        return await event.message.reply(
            message="You are not in the allowed list of users who can use me.",
            link_preview=False,
            parse_mode=html
        )
    await event.message.reply(
        message=f'Hi <a href="tg://user?id={event.chat_id}">{event.chat.first_name}</a>, Send me a file to get an instant stream link.',
        link_preview=False,
        parse_mode=html
    )

@StreamBot.on(NewMessage(incoming=True,pattern=r"^\/about*", func=lambda e: e.is_private))
async def about(event: NewMessage.Event):
    await event.message.reply(
        message=f"""
Maintained By: <a href="https://github.com/DeekshithSH">DeekshithSH</a>
Source Code: <a href="https://github.com/SpringsFern/TG-FileStreamBot">TG-FileStreamBot</a>
Based On: [<a href="bit.ly/tg-stream">tg filestream</a>] [<a href="https://github.com/EverythingSuckz/TG-FileStreamBot">TG-FileStreamBot</a>]
Version: {__version__}
Last Updated: 15 March 20225
""",
        link_preview=False,
        parse_mode=html
    )