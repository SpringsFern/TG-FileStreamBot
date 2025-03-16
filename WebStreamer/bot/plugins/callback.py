# This file is a part of TG-FileStreamBot

from telethon.events import CallbackQuery
from telethon.extensions import html

from WebStreamer import __version__
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.translation import Text, BUTTON

@StreamBot.on(CallbackQuery())
async def cb_data(event: CallbackQuery.Event) -> None:
    usr_cmd:list[str] = event.data.decode("utf-8").split("_")
    if usr_cmd[0] == "home":
        await event.edit(
            text=Text.START_TEXT.format(event.chat_id, getattr(event.chat, "first_name")),
            buttons=BUTTON.START_BUTTONS,
            link_preview=False,
            parse_mode=html
        )
    elif usr_cmd[0] == "help":
        await event.edit(
            text=Text.HELP_TEXT.format(Var.UPDATES_CHANNEL),
            buttons=BUTTON.HELP_BUTTONS,
            link_preview=False,
            parse_mode=html
        )
    elif usr_cmd[0] == "about":
        await event.edit(
            text=Text.ABOUT_TEXT.format(__version__),
            buttons=BUTTON.ABOUT_BUTTONS,
            link_preview=False,
            parse_mode=html
        )
    elif usr_cmd[0] == "N/A":
        await event.answer("N/A")
    elif usr_cmd[0] == "close":
        await event.delete()
