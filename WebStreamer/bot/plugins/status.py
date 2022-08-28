# This file is a part of TG-FileStreamBot

import time
import shutil
import psutil
from WebStreamer import StartTime
from WebStreamer.bot import StreamBot
from pyrogram import filters, Client
from pyrogram.types import Message
from WebStreamer.utils.Translation import Language
from WebStreamer.utils.time_format import get_readable_time
from WebStreamer.utils.human_readable import humanbytes
from pyrogram.enums.parse_mode import ParseMode

@StreamBot.on_message(filters.command('status') & filters.private)
async def start(b: Client, m: Message):
    lang = Language(m)

    uptime = get_readable_time((time.time() - StartTime))
    total, used, free = shutil.disk_usage('.')

    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)

    sent = humanbytes(psutil.net_io_counters().bytes_sent)
    recv = humanbytes(psutil.net_io_counters().bytes_recv)

    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    sys_stat = f"""<b>Bot Uptime:</b> {uptime}
<b>Total disk space:</b> {total}
<b>Used:</b> {used}
<b>Free:</b> {free}\n
📊Data Usage📊\n<b>Upload:</b> {sent}
<b>Down:</b> {recv}\n
<b>CPU:</b> {cpuUsage}% 
<b>RAM:</b> {memory}% 
<b>Disk:</b> {disk}%"""

    await m.reply_text(
        text=sys_stat,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
        )