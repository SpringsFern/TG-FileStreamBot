from WebStreamer.vars import Var
from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyrogram import Client, filters
from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
db = Database(Var.DATABASE_URL, Var.SESSION_NAME)

SETTINGS_TEXT = """
<b>Settings</b>
<i>🔸Select an option from keyboard</i>
"""
SETTINGS_BTN=ReplyKeyboardMarkup(
        [
            ["🔗Link Type"],
            ["📚Help","⚙️Close","status📊"]
        ],
        resize_keyboard=True
    )
SETTINGS_LinkType_BTN=ReplyKeyboardMarkup(
        [
            ["🔗With Name","🔗Without Name","🔗Current Type"]
        ],
        resize_keyboard=True
    )

@StreamBot.on_message(filters.private & filters.command("settings"))
async def start(b: Client, m: Message):
    if await db.is_user_banned(m.from_user.id):
        await b.send_message(
                chat_id=m.chat.id,
                text="__Sᴏʀʀʏ Sɪʀ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴛʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ__\n\n @DeekshithSH **Tʜᴇʏ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ**",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
        await b.send_message(
                Var.BIN_CHANNEL,
                f"**Banned User** [{m.from_user.first_name}](tg://user?id={m.from_user.id}) **Trying to Access the bot \nUser ID: {m.chat.id}**"
            )
        return
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nᴇᴡ Usᴇʀ Jᴏɪɴᴇᴅ:** \n\n__Mʏ Nᴇᴡ Fʀɪᴇɴᴅ__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sᴛᴀʀᴛᴇᴅ Yᴏᴜʀ Bᴏᴛ !!__"
        )
    user, in_db = await db.Current_Settings_Link(m.from_user.id)
    if not in_db:
        await db.setttings_default(m.from_user.id)
        await m.reply_text(text="Created Settings in DB")
    await m.reply_text(
        text=SETTINGS_TEXT,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=SETTINGS_BTN
        )

@StreamBot.on_message(filters.private & filters.regex("⚙️Close") & ~filters.edited)
async def close_settings(b, m):
    await m.reply_text(
    text="Settings Closed",
    parse_mode="HTML",
    disable_web_page_preview=True,
    reply_markup=ReplyKeyboardRemove(True)
    )

@StreamBot.on_message(filters.private & filters.regex("🔗Link Type") & ~filters.edited)
async def close_settings(b, m):
    await m.reply_text(
    text="Select Link Type",
    parse_mode="HTML",
    disable_web_page_preview=True,
    reply_markup=SETTINGS_LinkType_BTN
    )

@StreamBot.on_message(filters.private & filters.regex("🔗With Name") & ~filters.edited)
async def close_settings(b, m: Message):
    try:
        user, in_db = await db.Current_Settings_Link(m.from_user.id)
        if not in_db:
            await m.reply_text(text="First Send /settings then use This Keyword")
            return
        await db.Settings_Link_WithName(m.from_user.id)
        user, in_db = await db.Current_Settings_Link(m.from_user.id)

        await m.reply_text(
        text=f"Link With FileName: `{user['LinkWithName']}`",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=ReplyKeyboardRemove(True)
        )
    except Exception as e:
        await m.reply_text(
        text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`\n#Settings",
        disable_web_page_preview=True,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(True)
        )

@StreamBot.on_message(filters.private & filters.regex("🔗Without Name") & ~filters.edited)
async def close_settings(b, m):
    try:
        user, in_db = await db.Current_Settings_Link(m.from_user.id)
        if not in_db:
            await m.reply_text(text="First Send /settings then use This Keyword")
            return
        await db.Settings_Link_WithoutName(m.from_user.id)
        user, in_db = await db.Current_Settings_Link(m.from_user.id)

        await m.reply_text(
        text=f"Link With FileName: `{user['LinkWithName']}`",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=ReplyKeyboardRemove(True)
        )
    except Exception as e:
        await m.reply_text(
        text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`\n#Settings",
        disable_web_page_preview=True,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(True)
        )

@StreamBot.on_message(filters.private & filters.regex("🔗Current Type") & ~filters.edited)
async def close_settings(b, m):
    try:
        settings, in_db = await db.Current_Settings_Link(m.from_user.id)
        if not in_db:
            await m.reply_text(text="First Send /settings then use This Keyword")
            return
        await m.reply_text(
        text=f"Link With Name: `{settings['LinkWithName']}`",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=ReplyKeyboardRemove(True)
        )
    except Exception as e:
        await m.reply_text(
        text=f"**#ᴇʀʀᴏʀ_ᴛʀᴀᴄᴇʙᴀᴄᴋ:** `{e}`\n#Settings",
        disable_web_page_preview=True,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(True)
        )