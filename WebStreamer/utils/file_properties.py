# import mimetypes
# import urllib.parse

import asyncio
from typing import Any
from urllib.parse import quote_plus
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyrogram import Client
from pyrogram.methods import Messages

from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.vars import Var

import WebStreamer.utils.Translation as Translation
from WebStreamer.utils.database import Database
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

# def mimetype(filename):
#     mimetypes.init()
#     mimestart = mimetypes.guess_type(filename)[0]

#     if mimestart != None:
#         mimestart = mimestart.split('/')[0]

#         return mimestart
#     else:
#         return "None"

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media

def get_media_file_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    FileName=getattr(media, "file_name", "None")
    if FileName:
        return FileName
    else:
        return ""

def get_media_file_size(m):
    media = get_media_from_message(m)
    return getattr(media, "file_size", "None")

def get_media_mime_type(m):
    media = get_media_from_message(m)
    return getattr(media, "mime_type", "None/unknown")

def get_media_file_unique_id(m):
    media = get_media_from_message(m)
    return getattr(media, "file_unique_id", "")

def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]

# Generate Text, Stream Link, reply_markup
async def gen_link(log_msg: Messages, from_channel: bool):
    """Generate Text for Stream Link, Reply Text and reply_markup"""
    # lang = getattr(Translation, message.from_user.language_code)
    lang = getattr(Translation, "en")
    file_name = get_media_file_name(log_msg)
    file_size = humanbytes(get_media_file_size(log_msg))
    
    if Var.PAGE_LINK:
        page_link = f"https://{Var.PAGE_LINK}/?id={log_msg.message_id}&type={get_media_mime_type(log_msg)}"
    else:
        page_link = f"{Var.URL}watch/{log_msg.message_id}"

    stream_link = f"{Var.URL}{log_msg.message_id}/{quote_plus(get_media_file_name(log_msg))}"
    Stream_Text = lang.stream_msg_text.format(file_name, file_size, stream_link, page_link)
    if from_channel:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥STREAM", url=page_link), InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ 📥", url=stream_link)]])
    else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥STREAM", url=page_link), InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ 📥", url=stream_link)],
            [InlineKeyboardButton("❌ Delete Link", callback_data=f"msgdelconf2_{log_msg.message_id}_{get_media_file_unique_id(log_msg)}")]])
    
    return str(Stream_Text), reply_markup, str(stream_link)
