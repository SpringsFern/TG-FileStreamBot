# Taken from megadlbot_oss <https://github.com/eyaadh/megadlbot_oss/blob/master/mega/webserver/routes.py>
# Thanks to Eyaadh <https://github.com/eyaadh>

import time
import logging
import mimetypes
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from WebStreamer.bot import multi_clients, work_loads, BotInfo
from WebStreamer.utils.file_properties import get_short_hash, pack_file
from WebStreamer.utils.util import allow_request, get_requester_ip, get_readable_time
from WebStreamer.vars import Var
from WebStreamer.server.exceptions import FIleNotFound, InvalidHash
from WebStreamer import StartTime, __version__
from WebStreamer.utils.paralleltransfer import ParallelTransferrer


routes = web.RouteTableDef()
class_cache = {}

@routes.get("/status", allow_head=True)
async def root_route_handler(_: web.Request):
    return web.json_response(
        {
            "server_status": "running",
            "uptime": get_readable_time(time.time() - StartTime),
            "telegram_bot": "@" + BotInfo.username,
            "connected_bots": len(multi_clients),
            "loads": dict(
                ("bot" + str(c + 1), l)
                for c, (_, l) in enumerate(
                    sorted(work_loads.items(),
                           key=lambda x: x[1], reverse=True)
                )
            ),
            "version": __version__,
        }
    )


@routes.get(r"/stream/{messageID:\d+}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        message_id = int(request.match_info["messageID"])
        secure_hash = request.rel_url.query.get("hash")
        return await media_streamer(request, message_id, secure_hash)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        logging.critical(str(e), exc_info=True)
        raise web.HTTPInternalServerError(text=str(e))


async def media_streamer(request: web.Request, message_id: int, secure_hash: str):
    head: bool = request.method == "HEAD"
    ip = get_requester_ip(request)
    range_header = request.headers.get("Range", 0)

    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]

    if Var.MULTI_CLIENT:
        logging.debug("Client %s is now serving %s", index, ip)

    if faster_client in class_cache:
        transfer = class_cache[faster_client]
        logging.debug("Using cached ByteStreamer object for client %s", index)
    else:
        logging.debug("Creating new ByteStreamer object for client %s", index)
        transfer = ParallelTransferrer(faster_client)
        transfer.post_init()
        class_cache[faster_client] = transfer
        logging.debug("Created new ByteStreamer object for client %s", index)
    logging.debug("before calling get_file_properties")
    try:
        file_id = await transfer.get_file_properties(message_id)
    except FIleNotFound:
        return web.Response(status=404, text="File not found")

    full_hash = pack_file(
        file_id.file_name,
        file_id.file_size,
        file_id.mime_type,
        file_id.id
    )
    if get_short_hash(full_hash) != secure_hash:
        logging.debug("Invalid hash for message with ID %s", message_id)
        raise InvalidHash

    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )
    until_bytes = min(until_bytes, file_size - 1)
    req_length = until_bytes - from_bytes + 1
    if not head:
        if not allow_request(ip):
            return web.Response(status=429)
        body = transfer.download(
            file_id, file_size, from_bytes, until_bytes, index, ip
        )
    else:
        body = None

    mime_type = file_id.mime_type
    file_name = file_id.file_name
    disposition = "attachment"

    if not mime_type:
        mime_type = mimetypes.guess_type(
            file_name)[0] or "application/octet-stream"

    if ("video/" in mime_type or "audio/" in mime_type) and Var.STREAM_MEDIA:
        disposition = "inline"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )
