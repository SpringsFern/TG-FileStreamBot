# This file is a part of TG-FileStreamBot

from __future__ import annotations
import hashlib
import logging
from typing import List
from telethon import TelegramClient
from telethon.tl import types
from telethon.tl.custom.file import File
from telethon.tl.patched import Message
from telethon.tl.types import InputDocumentFileLocation, InputPhotoFileLocation
from WebStreamer.server.exceptions import FIleNotFound
from WebStreamer.vars import Var

class FileInfo:
    file_size: int = None
    mime_type: str = None
    file_name: str = None
    id: int = None
    dc_id: int = None
    location: types.InputPhotoFileLocation | types.InputDocumentFileLocation = None

class HashableFileStruct:
    def __init__(self, file_name: str, file_size: int, mime_type: str, file_id: int):
        self.file_name = file_name
        self.file_size = file_size
        self.mime_type = mime_type
        self.file_id = file_id

    def pack(self) -> str:
        hasher = hashlib.md5()
        fields = [self.file_name, str(self.file_size), self.mime_type, str(self.file_id)]

        for field in fields:
            hasher.update(field.encode())

        return hasher.hexdigest()

async def get_file_ids(client: TelegramClient, chat_id: int, message_id: int) -> FileInfo:
    message: Message = await client.get_messages(chat_id, ids=message_id)
    if not message:
        logging.debug("Message with ID %s not found",message_id)
        raise FIleNotFound
    return get_file_info(message)

def get_file_info(message: Message) -> FileInfo:
    media: types.MessageMediaDocument|types.MessageMediaPhoto = message.media
    file_id=FileInfo()
    file_id.file_size=get_size(media)
    file_id.mime_type=message.file.mime_type
    file_id.file_name=get_name(message.file)
    file_id.id=get_media_id(media)

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
        main=get_photo(file)
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
        file_name=media.name or ""
        return file_name
    except Exception as e:
        logging.error(e)
        logging.info("ErrorGettingFileName: %s",media)
        return "None"

def get_size(file: types.MessageMediaDocument|types.MessageMediaPhoto) -> int:
    if isinstance(file, types.MessageMediaDocument):
        return getattr(file.document,"size", 0)
    elif isinstance(file, types.MessageMediaPhoto):
        main = get_photo(file.photo)
        return main.size

def get_photo(file: types.MessageMediaPhoto) -> types.PhotoSize:
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
    return photos[-1]


def get_media_id(media: types.MessageMediaDocument|types.MessageMediaPhoto) -> int:
    if isinstance(media, types.MessageMediaDocument):
        return media.document.id
    elif isinstance(media, types.MessageMediaPhoto):
        return media.photo.id
    else:
        return 0

def pack_file(file_name: str, file_size: int, mime_type: str, file_id: int) -> str:
    return HashableFileStruct(file_name, file_size, mime_type, file_id).pack()

def get_short_hash(file_hash: str) -> str:
    return file_hash[:Var.HASH_LENGTH]
