# (c) @Avishkarpatil

import asyncio

from pyrogram.types.messages_and_media import video
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.mimetype.py import isMediaFile
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


print("stream.py started")
msg_text ="""
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n
<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n
<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n
<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n
<b>🚸 Nᴏᴛᴇ : Tʜɪs ᴘᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ, Nᴏᴛ Exᴘɪʀᴇᴅ</b>\n"""

msgs_text ="""
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n
<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n
<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n
<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n
<b>🌐 Download Page :</b> <i>{}</i>\n
<b>🚸 Nᴏᴛᴇ : Tʜɪs ᴘᴇʀᴍᴀɴᴇɴᴛ Lɪɴᴋ, Nᴏᴛ Exᴘɪʀᴇᴅ</b>\n"""

@StreamBot.on_message(filters.private & (filters.document | filters.video | filters.audio) & ~filters.edited, group=4)
async def private_receive_handler(b, m: Message,):
    if await db.is_user_banned(m.from_user.id):
        await b.send_message(
                chat_id=m.chat.id,
                text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @DeekshithSH **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
        await b.send_message(
                Var.BIN_CHANNEL,
                f"**Banned User** [{m.from_user.first_name}](tg://user?id={m.from_user.id}) **Trying to Access the bot \n User ID: {m.chat.id,}**"
            )
    else:
        if not await db.is_user_exist(m.from_user.id):
            await db.add_user(m.from_user.id)
            await b.send_message(
                Var.BIN_CHANNEL,
                f"Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ : \n\nNᴀᴍᴇ : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!"
            )
        try:
            # Forwarding Message to Bin Channel
            log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

            stream_link = "https://{}/{}".format(Var.FQDN, log_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
                "http://{}:{}/{}".format(Var.FQDN,
                                        Var.PORT,
                                        log_msg.message_id)

            file_size = None
            if m.video:
                file_size = f"{humanbytes(m.video.file_size)}"
            elif m.document:
                file_size = f"{humanbytes(m.document.file_size)}"
            elif m.audio:
                file_size = f"{humanbytes(m.audio.file_size)}"

            file_name = None
            if m.video:
                file_name = f"{m.video.file_name}"
            elif m.document:
                file_name = f"{m.document.file_name}"
            elif m.audio:
                file_name = f"{m.audio.file_name}"

            # Stream Page Link If Link is Available
            if Var.PAGE_LINK:
                media_type=isMediaFile(file_name)
                page_link = "https://{}/?id={}&type={}".format(Var.PAGE_LINK, log_msg.message_id, media_type)
                
            # adding Download Link to Mongodb only message_id
            await db.user_data(m.from_user.id, log_msg.message_id, file_name, file_size)
            # Replying to File Sent by Bot to Bin Channel
            await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
            
            # Sending Download Link, File Size, File Name to User
            if Var.PAGE_LINK:
                await m.reply_text(
                    text=msgs_text.format(file_name, file_size, stream_link, page_link),
                    parse_mode="HTML", 
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥", url=stream_link)]]),
                    quote=True
                )
            else:
                await m.reply_text(
                    text=msg_text.format(file_name, file_size, stream_link),
                    parse_mode="HTML", 
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥", url=stream_link)]]),
                    quote=True
                )
        except FloodWait as e:
            print(f"Sleeping for {str(e.x)}s")
            await asyncio.sleep(e.x)
            await b.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**𝚄𝚜𝚎𝚛 𝙸𝙳 :** `{str(m.from_user.id)}`", disable_web_page_preview=True, parse_mode="Markdown")
