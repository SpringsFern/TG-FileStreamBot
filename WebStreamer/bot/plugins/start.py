# This file is a part of FileStreamBot

from telethon.extensions import html
from telethon.events import NewMessage
from WebStreamer import __version__
from WebStreamer.bot import StreamBot
from WebStreamer.utils.utils import validate_user
from WebStreamer.vars import Var
from WebStreamer.utils.translation import Text, BUTTON

@StreamBot.on(NewMessage(incoming=True,pattern=r"^\/start*"))
async def start(event: NewMessage.Event):
    if not await validate_user(event):
        return
    await event.message.reply(
        message=Text.START_TEXT.format(event.chat_id, event.chat.first_name),
        link_preview=False,
        buttons=BUTTON.START_BUTTONS,
        parse_mode=html
    )

@StreamBot.on(NewMessage(incoming=True,pattern=r"^\/about*"))
async def about(event: NewMessage.Event):
    if not await validate_user(event):
        return
    await event.message.reply(
        message=Text.ABOUT_TEXT.format(__version__),
        link_preview=False,
        buttons=BUTTON.ABOUT_BUTTONS,
        parse_mode=html
    )


@StreamBot.on(NewMessage(incoming=True,pattern=r"^\/help*"))
async def help_handler(event: NewMessage.Event):
    if not await validate_user(event):
        return
    await event.message.reply(
        message=Text.HELP_TEXT.format(Var.UPDATES_CHANNEL),
        buttons=BUTTON.HELP_BUTTONS,
        parse_mode=html,
        link_preview=False
        )
