# This file is a part of TG-FileStreamBot

from __future__ import annotations
import hashlib
import logging
from datetime import datetime
from typing import List
from telethon import TelegramClient
from telethon.tl import types
from telethon.tl.custom.file import File
from telethon.tl.patched import Message
from telethon.tl.types import InputDocumentFileLocation, InputPhotoFileLocation
from WebStreamer.server.exceptions import FIleNotFound
from WebStreamer.utils.file_id import FileUniqueId, FileUniqueType

class FileInfo:
    file_size: int = None
    mime_type: str = None
    file_name: str = None
    unique_id: str = None
    dc_id: int = None
    location: types.InputPhotoFileLocation | types.InputDocumentFileLocation = None

async def get_file_ids(client: TelegramClient, chat_id: int, message_id: int) -> FileInfo:
    message: Message = await client.get_messages(chat_id, ids=message_id)
    if not message:
        logging.debug("Message with ID %s not found",message_id)
        raise FIleNotFound

    media: types.MessageMediaDocument|types.MessageMediaPhoto = message.media
    file_id=FileInfo()
    file_id.file_size=get_size(media)
    file_id.mime_type=message.file.mime_type
    file_id.file_name=get_name(message.file)
    file_id.unique_id=get_file_unique_id(media)

    if isinstance(media, types.MessageMediaDocument):
        file: types.Document=media.document
        thumbnail_size=""
        file_id.location = InputDocumentFileLocation(
            id=file.id,
            access_hash=file.access_hash,
            file_reference=file.file_reference,
            thumb_size="",
        )
    elif isinstance(media, types.MessageMediaPhoto):
        file: types.Photo=media.photo
        photos: List[types.PhotoSize] = []
        for p in file.sizes:
            if isinstance(p, types.PhotoSize):
                photos.append(p)

            if isinstance(p, types.PhotoSizeProgressive):
                photos.append(
                    types.PhotoSize(
                        type=p.type,
                        w=p.w,
                        h=p.h,
                        size=max(p.sizes)
                    )
                )
        photos.sort(key=lambda p: p.size)
        main = photos[-1]

        thumbnail_size=main.type
        file_id.location = InputPhotoFileLocation(
            id=file.id,
            access_hash=file.access_hash,
            file_reference=file.file_reference,
            thumb_size=thumbnail_size,
        )

    file_id.dc_id=file.dc_id

    return file_id

def get_name(media: File) -> str:
    try:
        file_name=media.name
        if not file_name:
            date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"{date}{media.ext}"
        return file_name
    except Exception as e:
        logging.error(e)
        logging.info("ErrorGettingFileName: %s",media)
        return "None"

def get_file_unique_id(file: types.MessageMediaDocument|types.MessageMediaPhoto) -> str:
    if isinstance(file, types.MessageMediaDocument):
        document: types.Document=file.document
        return FileUniqueId(
            file_unique_type=FileUniqueType.DOCUMENT,
            media_id=document.id
        ).encode()

    elif isinstance(file, types.MessageMediaPhoto):
        photo: types.Photo=file.photo
        return FileUniqueId(
            file_unique_type=FileUniqueType.DOCUMENT,
            media_id=photo.id
        ).encode()

def get_size(file: types.MessageMediaDocument|types.MessageMediaPhoto) -> int:
    if isinstance(file, types.MessageMediaDocument):
        return getattr(file.document,"size", 0)
    elif isinstance(file, types.MessageMediaPhoto):
        photos: List[types.PhotoSize] = []
        for p in file.photo.sizes:
            if isinstance(p, types.PhotoSize):
                photos.append(p)

            if isinstance(p, types.PhotoSizeProgressive):
                photos.append(
                    types.PhotoSize(
                        type=p.type,
                        w=p.w,
                        h=p.h,
                        size=max(p.sizes)
                    )
                )
        photos.sort(key=lambda p: p.size)
        main = photos[-1]
        return main.size

def get_hash(file: types.MessageMediaDocument|types.MessageMediaPhoto, length: int) -> str:
    if isinstance(file, str):
        unique_id = file
    else:
        unique_id = get_file_unique_id(file)
    long_hash = hashlib.sha256(unique_id.encode("UTF-8")).hexdigest()
    return long_hash[:length]
