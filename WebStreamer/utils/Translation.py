# This file is a part of FileStreamBot

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from WebStreamer.vars import Var

class Language:
    def __new__(cls, message: Message):
        return getattr(cls, getattr(message.from_user, 'language_code', "en"), cls.en)

    available = ['en', 'language_code']

    class en:
        START_TEXT: str = """
<i>👋 Hey,</i>{}\n
<i>I'm Telegram Files Streaming Bot as well as a Direct Links Generator</i>\n
<i>Click on Help to get more information</i>\n
<i><u>WARNING 🚸</u></i>\n
<b>🔞 Adult content leads to a permanent ban.</b>\n\n"""

        HELP_TEXT: str = """
<i>- Send me any file (or) media from Telegram.</i>
<i>- I will provide an external direct download link!</i>
<i>- Download link with the fastest speed</i>
<u>🔸 WARNING 🚸</u>\n
<b>🔞 Adult content leads to a permanent ban.</b>\n
<i>Contact developer (or) report bugs</i> <b>: <a href='https://t.me/{}'>[ Click Here ]</a></b>"""

        ABOUT_TEXT: str = """
Maintained By: <a href="https://github.com/DeekshithSH">DeekshithSH</a>
Source Code: <a href="https://github.com/SpringsFern/TG-FileStreamBot">TG-FileStreamBot</a>
Based On: [<a href="bit.ly/tg-stream">tg filestream</a>] [<a href="https://github.com/EverythingSuckz/TG-FileStreamBot">TG-FileStreamBot</a>]
Version: {}
Last Updated: 23 March 20225
"""

        STREAM_MSG_TEXT: str = """
<i><u>Your Link Generated!</u></i>\n
<b>📂 File Name:</b> <i>{}</i>\n
<b>📦 File Size:</b> <i>{}</i>\n
<b>📥 Download:</b> <i>{}</i>\n
<b>🖥 Watch:</b> <i>{}</i>\n
<b>Link Generated Using</b> <a href='https://t.me/{}'>{}</a>"""

        BAN_TEXT: str = "__Sorry sir, you are banned from using me.__\n\n**[Contact Developer](tg://user?id={}) They will help you**"

        LINK_LIMIT_EXCEEDED: str = "You have exceeded the number of links you can generate."

        INFO_TEXT: str = """User ID: <code>{}</code>
Plan: <code>{}</code>
Links Used: <code>{}</code>
Links Left: <code>{}</code>"""

#----------------------#
# Change the Text's below to add suport for your language

# you can find the language_code for your language here
# https://en.wikipedia.org/wiki/IETF_language_tag#List_of_common_primary_language_subtags
# change language_code with your language code
# eg:    class kn(object):
    class language_code:
        START_TEXT: str = """
<i>👋 Hey,</i>{}\n
<i>I'm Telegram Files Streaming Bot as well as a Direct Links Generator</i>\n
<i>Click on Help to get more information</i>\n
<i><u>WARNING 🚸</u></i>\n
<b>🔞 Adult content leads to a permanent ban.</b>\n\n"""

        HELP_TEXT: str = """
<i>- Send me any file (or) media from Telegram.</i>
<i>- I will provide an external direct download link!</i>
<i>- Download link with the fastest speed</i>
<u>🔸 WARNING 🚸</u>\n
<b>🔞 Adult content leads to a permanent ban.</b>\n
<i>Contact developer (or) report bugs</i> <b>: <a href='https://t.me/{}'>[ Click Here ]</a></b>"""

        ABOUT_TEXT: str = """
Maintained By: <a href="https://github.com/DeekshithSH">DeekshithSH</a>
Source Code: <a href="https://github.com/SpringsFern/TG-FileStreamBot">TG-FileStreamBot</a>
Based On: [<a href="bit.ly/tg-stream">tg filestream</a>] [<a href="https://github.com/EverythingSuckz/TG-FileStreamBot">TG-FileStreamBot</a>]
Version: {}
Last Updated: 23 March 20225
"""

        STREAM_MSG_TEXT: str = """
<i><u>Your Link Generated!</u></i>\n
<b>📂 File Name:</b> <i>{}</i>\n
<b>📦 File Size:</b> <i>{}</i>\n
<b>📥 Download:</b> <i>{}</i>\n
<b>🖥 Watch:</b> <i>{}</i>\n
<b>Link Generated Using</b> <a href='https://t.me/{}'>{}</a>"""

        BAN_TEXT: str = "__Sorry sir, you are banned from using me.__\n\n**[Contact Developer](tg://user?id={}) They will help you**"

        LINK_LIMIT_EXCEEDED: str = "You have exceeded the number of links you can generate."

        INFO_TEXT: str = """User ID: <code>{}</code>
Plan: <code>{}</code>
Links Used: <code>{}</code>
Links Left: <code>{}</code>"""

class BUTTON(object):
    START_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ])

    HELP_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close'),
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ])

    ABOUT_BUTTONS = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close'),
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ])
