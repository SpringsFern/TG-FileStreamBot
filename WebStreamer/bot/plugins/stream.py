# (c) @Avishkarpatil

import yt_dlp
from WebStreamer.utils.mimetype import isMediaFile
import asyncio
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.vars import Var
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)


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

msg24_text ="""
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n
<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n
<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n
<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n
<b>🚸 Nᴏᴛᴇ : Don't Know when This Link Will Expire</b>\n"""

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
        if Var.FORCE_UPDATES_CHANNEL:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ.__\n\n  **Cᴏɴᴛᴀᴄᴛ Dᴇᴠᴇʟᴏᴘᴇʀ @DeekshithSH Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="""<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜꜱᴇ ᴍᴇ 🔐</i>""",
                    reply_markup=InlineKeyboardMarkup(
                        [[ InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}") ]]
                    ),
                    parse_mode="HTML"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ʙᴏss** @DeekshithSH",
                    parse_mode="markdown",
                    disable_web_page_preview=True)
                return

        try:
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
                if not await db.is_user_in_24hour(m.from_user.id):
                    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
                    stream_link = "https://{}/{}".format(Var.FQDN, log_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
                        "http://{}:{}/{}".format(Var.FQDN,
                                                Var.PORT,
                                                log_msg.message_id)
                else:
                    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL24)
                    stream_link = "https://{}/24/{}/{}".format(Var.FQDN, m.chat.id, m.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
                        "http://{}:{}/24/{}/{}".format(Var.FQDN,
                                                Var.PORT,
                                                m.chat.id,
                                                m.message_id)

                if Var.PAGE_LINK:
                    page_link = "https://{}/?id={}".format(Var.PAGE_LINK, log_msg.message_id)

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

                await db.user_data(m.from_user.id, log_msg.message_id, file_name, file_size)
                await log_msg.reply_text(text=f"**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`\n**Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ :** {stream_link}", disable_web_page_preview=True, parse_mode="Markdown", quote=True)
                
                if await db.is_user_in_24hour(m.from_user.id):
                    await m.reply_text(
                        text=msg24_text.format(file_name, file_size, stream_link),
                        parse_mode="HTML", 
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ɴᴏᴡ 📥", url=stream_link)]]),
                        quote=True
                    )
                elif Var.PAGE_LINK:
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


@StreamBot.on_message(filters.channel & (filters.document | filters.video) & ~filters.edited)
async def channel_receive_handler(bot, broadcast):
    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        stream_link = "https://{}/{}".format(Var.FQDN, log_msg.message_id) if Var.ON_HEROKU or Var.NO_PORT else \
            "http://{}:{}/{}".format(Var.FQDN,
                                    Var.PORT,
                                    log_msg.message_id)
        await log_msg.reply_text(
            text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** {stream_link}",
            # text=f"**Cʜᴀɴɴᴇʟ Nᴀᴍᴇ:** `{broadcast.chat.title}`\n**Cʜᴀɴɴᴇʟ ID:** `{broadcast.chat.id}`\n**Rᴇǫᴜᴇsᴛ ᴜʀʟ:** https://t.me/FxStreamBot?start=DeekshithSH_{str(log_msg.message_id)}",
            quote=True,
            parse_mode="Markdown"
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=stream_link)]])
            # [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ 📥", url=f"https://t.me/FxStreamBot?start=DeekshithSH_{str(log_msg.message_id)}")]])
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"Gᴏᴛ FʟᴏᴏᴅWᴀɪᴛ ᴏғ {str(w.x)}s from {broadcast.chat.title}\n\n**Cʜᴀɴɴᴇʟ ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True, parse_mode="Markdown")
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`", disable_web_page_preview=True, parse_mode="Markdown")
        print(f"Cᴀɴ'ᴛ Eᴅɪᴛ Bʀᴏᴀᴅᴄᴀsᴛ Mᴇssᴀɢᴇ!\nEʀʀᴏʀ: {e}")

@StreamBot.on_message(filters.command('ydl') & filters.private & ~filters.edited)
def start(b, m):
    usr_cmd = m.text.split("/ydl ")[-1]
    if not usr_cmd == "/ydl":
        snt_msg=m.reply_text(
            text=usr_cmd
        )
        class MyLogger:
            def debug(self, msg):
                # For compatibility with youtube-dl, both debug and info are passed into debug
                # You can distinguish them by the prefix '[debug] '
                if msg.startswith('[debug] '):
                    pass
                else:
                    self.info(msg)

            def info(self, msg):
                pass
            
            def warning(self, msg):
                print(msg)
                global ytdlwarn
                ytdlwarn=msg
                pass
            
            def error(self, msg):
                print(msg)

        # ℹ️ See "progress_hooks" in the docstring of yt_dlp.YoutubeDL
        def my_hook(d):
            res=d
            if res['status'] == 'downloading':
                size=humanbytes(res['downloaded_bytes'])
                filename = res['filename'].split("Files/")[-1]
                b.edit_message_text(
                    message_id=snt_msg.message_id,
                    chat_id=m.chat.id,
                    text="File Name: {}\nDownloading: {}/{}  {} \nSpeed: {}\nETA: {}</u>".format(filename, size, res['_total_bytes_str'], res['_percent_str'], res['_speed_str'], res['_eta_str'])
                    )    
            elif res['status'] == 'finished':
                b.edit_message_text(
                    message_id=snt_msg.message_id,
                    chat_id=m.chat.id,
                    text="Download Finished \nNow Uploading to Telegram"
                    )


        def format_selector(ctx):
            """ Select the best video and the best audio that won't result in an mkv.
            This is just an example and does not handle all cases """

            # formats are already sorted worst to best
            formats = ctx.get('formats')[::-1]

            # acodec='none' means there is no audio
            best_video = next(f for f in formats
                              if f['vcodec'] != 'none' and f['acodec'] == 'none')

            # find compatible audio extension
            audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
            # vcodec='none' means there is no video
            best_audio = next(f for f in formats if (
                f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

            yield {
                # These are the minimum required fields for a merged format
                'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
                'ext': best_video['ext'],
                'requested_formats': [best_video, best_audio],
                # Must be + separated list of protocols
                'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
            }


        # ℹ️ See docstring of yt_dlp.YoutubeDL for a description of the options
        ydl_opts = {
            'postprocessors': [{
                # Embed metadata in video using ffmpeg.
                # ℹ️ See yt_dlp.postprocessor.FFmpegMetadataPP for the arguments it accepts
                'key': 'FFmpegMetadata',
                'add_chapters': True,
                'add_metadata': True,
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'outtmpl': 'Files/%(title)s-%(id)s.%(ext)s',
            'restrictfilenames': True
        }


        # Add custom headers
        yt_dlp.utils.std_headers.update({'Referer': 'https://www.google.com'})

        # ℹ️ See the public functions in yt_dlp.YoutubeDL for for other available functions.
        # Eg: "ydl.download", "ydl.download_with_info_file"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(usr_cmd)

            # ℹ️ ydl.sanitize_info makes the info json-serializable
            # print(json.dumps(ydl.sanitize_info(info)))
            filename = ydl.prepare_filename(info)
            filename2=filename.split(".")[0]
            mediatype=isMediaFile(filename)

            try:
                if mediatype == 'audio':
                    b.send_audio(
                        chat_id=m.chat.id,
                        audio=filename,
                        # caption=filename,
                        reply_to_message_id=snt_msg.message_id
                    )
                elif mediatype == 'video':
                    b.send_video(
                        chat_id=m.chat.id,
                        video=filename,
                        # caption=filename,
                        supports_streaming=True,
                        reply_to_message_id=snt_msg.message_id
                    )
                elif mediatype == 'image':
                    b.send_photo(
                        chat_id=m.chat.id,
                        photo=filename,
                        # caption=filename,
                        reply_to_message_id=snt_msg.message_id
                    )
            except:
                if ytdlwarn == 'Requested formats are incompatible for merge and will be merged into mkv.':
                    b.edit_message_text(
                        message_id=snt_msg.message_id,
                        chat_id=m.chat.id,
                        text="🔸 𝗪𝗔𝗥𝗡𝗜𝗡𝗚 🚸\n{}\n🔹Uploading File to Telegram".format(ytdlwarn)
                    )
                    b.send_video(
                        chat_id=m.chat.id,
                        video="{}.mkv".format(filename2),
                        supports_streaming=False,
                        # caption=filename,
                        reply_to_message_id=snt_msg.message_id
                    )
                else:
                    b.send_text(
                        chat_id=m.chat.id,
                        text=ytdlwarn
                    )

    else:
        b.send_message(
            chat_id=m.chat.id,
            text="abcd",
            parse_mode="markdown",
            disable_web_page_preview=True
        )