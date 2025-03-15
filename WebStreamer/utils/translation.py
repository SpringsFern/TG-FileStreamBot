# This file is a part of FileStreamBot

from telethon import Button
from WebStreamer.vars import Var

class Text:
    START_TEXT: str = """
👋 Hi there, <a href="tg://user?id={}">{}</a>!

I am the File Stream Bot, your go-to assistant for generating external download links from any file or media you send. 
Feel free to explore my features and see how I can make file sharing a breeze.

Here's what you can do:
- Send me any file or media, and I'll provide you with an external download link.
- Need help or have a question? Just click on the 'Help' button below for more information.
"""

    HELP_TEXT: str = """
- Send any file or media to me.
- I will provide an external download link.
- For support or to report a bug <b><a href='https://t.me/{}'>[ click here] </a></b>.
"""

    ABOUT_TEXT: str = """
<b>Maintained By:</b> <a href="https://github.com/DeekshithSH">DeekshithSH</a>
<b>Source Code:</b> <a href="https://github.com/SpringsFern/TG-FileStreamBot">TG-FileStreamBot</a>
<b>Based On:</b> [<a href="bit.ly/tg-stream">tg filestream</a>] [<a href="https://github.com/EverythingSuckz/TG-FileStreamBot">TG-FileStreamBot</a>]
<b>Version:</b> {}
<b>Last Updated:</b> 15 March 20225
"""

    STREAM_MSG_TEXT: str = """
<u><i>Your Link is Generated!</i></u>\n
<b>📂 File Name:</b> <i>{name}</i>\n
<b>📦 File Size:</b> <i>{size}</i>\n
<b>📥 Download:</b> <i>{link}</i>\n
Link generated using <a href='https://t.me/{username}'>{firstname}</a>
"""

class BUTTON(object):
    START_BUTTONS = [
        [
            Button.inline('Hᴇʟᴘ', 'help'),
            Button.inline('Aʙᴏᴜᴛ', 'about'),
            Button.inline('Cʟᴏsᴇ', 'close')
        ],
        [Button.url("📢 Bot Channel", f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ]
    HELP_BUTTONS = [
        [
            Button.inline('Hᴏᴍᴇ', 'home'),
            Button.inline('Aʙᴏᴜᴛ', 'about'),
            Button.inline('Cʟᴏsᴇ', 'close'),
        ],
        [Button.url("📢 Bot Channel", f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ]
    ABOUT_BUTTONS = [
        [
            Button.inline('Hᴏᴍᴇ', 'home'),
            Button.inline('Hᴇʟᴘ', 'help'),
            Button.inline('Cʟᴏsᴇ', 'close'),
        ],
        [Button.url("📢 Bot Channel", f'https://t.me/{Var.UPDATES_CHANNEL}')]
    ]
