# © @Avishkarpatil [ Telegram ]

from pyrogram import client
from pyrogram.client import Client
import yt_dlp
from WebStreamer.utils.mimetype import isMediaFile
from typing import Text
from WebStreamer.bot import StreamBot
from WebStreamer.vars import Var
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

print("start.py started")
START_TEXT = """
<i>👋 Hᴇʏ,</i>{}\n
<i>I'ᴍ Tᴇʟᴇɢʀᴀᴍ Fɪʟᴇs Sᴛʀᴇᴀᴍɪɴɢ Bᴏᴛ ᴀs ᴡᴇʟʟ Dɪʀᴇᴄᴛ Lɪɴᴋs Gᴇɴᴇʀᴀᴛᴇ</i>\n
<i>Cʟɪᴄᴋ ᴏɴ Hᴇʟᴘ ᴛᴏ ɢᴇᴛ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</i>\n
<i><u>𝗪𝗔𝗥𝗡𝗜𝗡𝗚 🚸</u></i>
<b>🔞 Pʀᴏɴ ᴄᴏɴᴛᴇɴᴛꜱ ʟᴇᴀᴅꜱ ᴛᴏ ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ ʏᴏᴜ.</b>\n\n"""

HELP_TEXT = """
<i>- Sᴇɴᴅ ᴍᴇ ᴀɴʏ ꜰɪʟᴇ (ᴏʀ) ᴍᴇᴅɪᴀ ꜰʀᴏᴍ ᴛᴇʟᴇɢʀᴀᴍ.</i>
<i>- I ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴇxᴛᴇʀɴᴀʟ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ !.</i>
<i>- Aᴅᴅ Mᴇ ɪɴ ʏᴏᴜʀ Cʜᴀɴɴᴇʟ Fᴏʀ Dɪʀᴇᴄᴛ Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋs Bᴜᴛᴛᴏɴ (add in channel not group. this bot will don't work on group)</i>
<i>- Tʜɪs Pᴇʀᴍᴇᴀɴᴛ Lɪɴᴋ Wɪᴛʜ Fᴀsᴛᴇsᴛ Sᴘᴇᴇᴅ</i>
<i>- you will get two links, one for download and the another for Download Page</i>
<i>  if first link is not working then Download from Download Page Link</i>
<b>- Try Using <a href="https://developers.cloudflare.com/1.1.1.1/setup-1.1.1.1">CloudFlare DNS</a> if see a Application error message</b>\n
<u>🔸 𝗪𝗔𝗥𝗡𝗜𝗡𝗚 🚸</u>\n
<b>🔞 Pʀᴏɴ ᴄᴏɴᴛᴇɴᴛꜱ ʟᴇᴀᴅꜱ ᴛᴏ ᴘᴇʀᴍᴀɴᴇɴᴛ ʙᴀɴ ʏᴏᴜ.</b>\n
<i>Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ (ᴏʀ) ʀᴇᴘᴏʀᴛ ʙᴜɢꜱ</i> <b>: <a href='https://t.me/DeekshithSH'>[ ᴄʟɪᴄᴋ ʜᴇʀᴇ ]</a></b>"""

ABOUT_TEXT = """
<b>⚜ Mʏ ɴᴀᴍᴇ : Public Link Generator</b>\n
<b>🔸Vᴇʀꜱɪᴏɴ : 3.0.3</b>\n
<b>>🔹Lᴀꜱᴛ ᴜᴘᴅᴀᴛᴇᴅ : [ 25-Dec-21 ] 06:55 PM</b>
"""

SETTINGS_TEXT = """
<b>Settings</b>
<i>🔸You Can edit Telegram Link Type, by clicking on the button below</i>
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close')
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
        ]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hᴏᴍᴇ', callback_data='home'),
        InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close'),
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
        ]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Hᴏᴍᴇ', callback_data='home'),
        InlineKeyboardButton('Hᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close'),
        ],
        [InlineKeyboardButton("📢 Bot Channel", url=f'https://t.me/{Var.UPDATES_CHANNEL}')]
        ]
    )
SETTINGS_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Permanent Link', callback_data='24link')
        ]]
    )
SETTINGS_BUTTONS24 = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Second Link', callback_data='permanentlink')
        ]]
    )

@StreamBot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data == "settings":
        await update.message.edit_text(
            text=SETTINGS_TEXT,
            disable_web_page_preview=True,
            reply_markup=SETTINGS_BUTTONS
        )
    elif update.data == "24link":
        if not await db.is_user_in_24hour(update.from_user.id):
            await db.add_user_in_24(update.from_user.id)
            await update.message.edit_text(
                text=SETTINGS_TEXT,
                disable_web_page_preview=True,
                reply_markup=SETTINGS_BUTTONS24
            )
    elif update.data == "permanentlink":
        await db.remove_user_from_24(update.from_user.id)
        await update.message.edit_text(
            text=SETTINGS_TEXT,
            disable_web_page_preview=True,
            reply_markup=SETTINGS_BUTTONS
        )
    else:
        await update.message.delete()


@StreamBot.on_message(filters.command('start') & filters.private & ~filters.edited)
async def start(b, m):
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
                f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
            )
        usr_cmd = m.text.split("_")[-1]
        if usr_cmd == "/start":
            if Var.FORCE_UPDATES_CHANNEL:
                try:
                    user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                    if user.status == "kicked":
                        await b.send_message(
                            chat_id=m.chat.id,
                            text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @DeekshithSH **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                            parse_mode="markdown",
                            disable_web_page_preview=True
                        )
                        return
                except UserNotParticipant:
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ 🔐</i>",
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                                ]]
                        ),
                        parse_mode="HTML"
                    )
                    return
                except Exception:
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<i>Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ</i> <b><a href='http://t.me/DeekshithSH'>[ ᴄʟɪᴄᴋ ʜᴇʀᴇ ]</a></b>",
                        parse_mode="HTML",
                        disable_web_page_preview=True)
                    return
            await m.reply_text(
                text=START_TEXT.format(m.from_user.mention),
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup=START_BUTTONS
                  )

@StreamBot.on_message(filters.private & filters.command(["about"]))
async def start(b ,m):
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
                f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
            )
        if Var.FORCE_UPDATES_CHANNEL:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @DeekshithSH **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode="HTML"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ</i> <b><a href='http://t.me/DeekshithSH'>[ ᴄʟɪᴄᴋ ʜᴇʀᴇ ]</a></b>",
                    parse_mode="HTML",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
        text=ABOUT_TEXT.format(m.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
            )

@StreamBot.on_message(filters.private & filters.command(["help"]))
async def start(b ,m):
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
                f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
            )
        if Var.FORCE_UPDATES_CHANNEL:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @DeekshithSH **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode="HTML"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ</i> <b><a href='http://t.me/DeekshithSH'>[ ᴄʟɪᴄᴋ ʜᴇʀᴇ ]</a></b>",
                    parse_mode="HTML",
                    disable_web_page_preview=True)
                return
        await m.reply_text(
        text=HELP_TEXT.format(m.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
            )

@StreamBot.on_message(filters.private & filters.command("settings"))
async def start(b, m):
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
                f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
            )
        if Var.FORCE_UPDATES_CHANNEL:
            try:
                user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                if user.status == "kicked":
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @DeekshithSH **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ 🔐</i>",
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                            ]]
                    ),
                    parse_mode="HTML"
                )
                return
            except Exception:
                await b.send_message(
                    chat_id=m.chat.id,
                    text="<i>Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ</i> <b><a href='http://t.me/DeekshithSH'>[ ᴄʟɪᴄᴋ ʜᴇʀᴇ ]</a></b>",
                    parse_mode="HTML",
                    disable_web_page_preview=True)
                return
        if await db.is_user_in_24hour(m.from_user.id):
            await m.reply_text(
                text=SETTINGS_TEXT,
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup=SETTINGS_BUTTONS24
                  )
        else:
            await m.reply_text(
                text=SETTINGS_TEXT,
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup=SETTINGS_BUTTONS
                )

@StreamBot.on_message(filters.command('name') & filters.private & ~filters.edited)
async def start(b, m):
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
                f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
            )
        usr_sent_name = m.text.split("/name ")[-1]
        if not usr_sent_name == "/name":
            if Var.FORCE_UPDATES_CHANNEL:
                try:
                    user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
                    if user.status == "kicked":
                        await b.send_message(
                            chat_id=m.chat.id,
                            text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @DeekshithSH **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                            parse_mode="markdown",
                            disable_web_page_preview=True
                        )
                        return
                except UserNotParticipant:
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<i>Jᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ 🔐</i>",
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton("Jᴏɪɴ ɴᴏᴡ 🔓", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                                ]]
                        ),
                        parse_mode="HTML"
                    )
                    return
                except Exception:
                    await b.send_message(
                        chat_id=m.chat.id,
                        text="<i>Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴅᴇᴠᴇʟᴏᴘᴇʀ</i> <b><a href='http://t.me/DeekshithSH'>[ ᴄʟɪᴄᴋ ʜᴇʀᴇ ]</a></b>",
                        parse_mode="HTML",
                        disable_web_page_preview=True)
                    return
    
            await b.send_message(
                    Var.OWNER_ID,
                    f"[{m.from_user.first_name}](tg://user?id={m.from_user.id}) **\n User ID: {m.chat.id} \n Suggest a Name \n {usr_sent_name}**"
                )  
            await m.reply_text(
                    text="Thank You for suggesting a name \n your suggested name sent to @DeekshithSH",
                    parse_mode="markdown",
                    disable_web_page_preview=True,
                    quote=True
                  )
        else:
            await m.reply_text(
                            text="you can suggest me a name with /name command \n eg: /name Direct Link Generator",
                            parse_mode="markdown",
                            disable_web_page_preview=True,
                            quote=True
                          )

@StreamBot.on_message(filters.command('ytdl') & filters.private & ~filters.edited)
def start(b, m):
    usr_cmd = m.text.split("/ytdl ")[-1]
    if not usr_cmd == "/ytdl":
        snt_msg=m.reply_text(
            text=usr_cmd
        )
        log_msg=b.send_message(text=f"**ʟɪɴᴋ :** {usr_cmd}\n**RᴇQᴜᴇꜱᴛᴇᴅ ʙʏ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uꜱᴇʀ ɪᴅ :** `{m.from_user.id}`", chat_id=Var.BIN_CHANNEL24, disable_web_page_preview=True, parse_mode="Markdown")
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
            'format': format_selector,
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

            def progress(current, total):
                b.edit_message_text(
                    message_id=snt_msg.message_id,
                    chat_id=m.chat.id,
                    text=f"{current * 100 / total:.1f}% uploaded"
                    )   

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
                        progress=progress,
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
                    log_msg.reply_text(text="{ytdlwarn}\n#ytdlp-error")

    else:
        b.send_message(
            chat_id=m.chat.id,
            text="Send me YouTube Link\nEg:/ytdl https://www.youtube.com/watch?v=BaW_jenozKc",
            parse_mode="markdown",
            disable_web_page_preview=True
        )
