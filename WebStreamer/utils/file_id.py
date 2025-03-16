#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import base64
import struct
from enum import IntEnum
from io import BytesIO
from typing import List, cast

class Bytes(bytes):
    @classmethod
    def read(cls, data: BytesIO) -> bytes:
        length = int.from_bytes(data.read(1), "little")

        if length <= 253:
            x = data.read(length)
            data.read(-(length + 1) % 4)
        else:
            length = int.from_bytes(data.read(3), "little")
            x = data.read(length)
            data.read(-length % 4)

        return x

    def __new__(cls, value: bytes) -> bytes:  # type: ignore
        length = len(value)

        if length <= 253:
            return (
                bytes([length])
                + value
                + bytes(-(length + 1) % 4)
            )
        else:
            return (
                bytes([254])
                + length.to_bytes(3, "little")
                + value
                + bytes(-length % 4)
            )

class String(Bytes):
    @classmethod
    def read(cls, data: BytesIO) -> str:  # type: ignore
        return cast(bytes, super(String, String).read(data)).decode(errors="replace")

    def __new__(cls, value: str) -> bytes:  # type: ignore
        return super().__new__(cls, value.encode())


def b64_encode(s: bytes) -> str:
    """Encode bytes into a URL-safe Base64 string without padding

    Parameters:
        s (``bytes``):
            Bytes to encode

    Returns:
        ``str``: The encoded bytes
    """
    return base64.urlsafe_b64encode(s).decode().strip("=")


def b64_decode(s: str) -> bytes:
    """Decode a URL-safe Base64 string without padding to bytes

    Parameters:
        s (``str``):
            String to decode

    Returns:
        ``bytes``: The decoded string
    """
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def rle_encode(s: bytes) -> bytes:
    """Zero-value RLE encoder

    Parameters:
        s (``bytes``):
            Bytes to encode

    Returns:
        ``bytes``: The encoded bytes
    """
    r: List[int] = []
    n: int = 0

    for b in s:
        if not b:
            n += 1
        else:
            if n:
                r.extend((0, n))
                n = 0

            r.append(b)

    if n:
        r.extend((0, n))

    return bytes(r)


def rle_decode(s: bytes) -> bytes:
    """Zero-value RLE decoder

    Parameters:
        s (``bytes``):
            Bytes to decode

    Returns:
        ``bytes``: The decoded bytes
    """
    r: List[int] = []
    z: bool = False

    for b in s:
        if not b:
            z = True
            continue

        if z:
            r.extend((0,) * b)
            z = False
        else:
            r.append(b)

    return bytes(r)

class FileUniqueType(IntEnum):
    """Known file unique types"""
    WEB = 0
    PHOTO = 1
    DOCUMENT = 2
    SECURE = 3
    ENCRYPTED = 4
    TEMP = 5


class FileUniqueId:
    def __init__(
        self, *,
        file_unique_type: FileUniqueType,
        url: str = None,
        media_id: int = None,
        volume_id: int = None,
        local_id: int = None
    ):
        self.file_unique_type = file_unique_type
        self.url = url
        self.media_id = media_id
        self.volume_id = volume_id
        self.local_id = local_id

    @staticmethod
    def decode(file_unique_id: str):
        buffer = BytesIO(rle_decode(b64_decode(file_unique_id)))
        file_unique_type, = struct.unpack("<i", buffer.read(4))

        try:
            file_unique_type = FileUniqueType(file_unique_type)
        except ValueError as e:
            raise ValueError(f"Unknown file_unique_type {file_unique_type} of file_unique_id {file_unique_id}") from e

        if file_unique_type == FileUniqueType.WEB:
            url = String.read(buffer)

            return FileUniqueId(
                file_unique_type=file_unique_type,
                url=url
            )

        if file_unique_type == FileUniqueType.PHOTO:
            volume_id, local_id = struct.unpack("<qi", buffer.read())

            return FileUniqueId(
                file_unique_type=file_unique_type,
                volume_id=volume_id,
                local_id=local_id
            )

        if file_unique_type == FileUniqueType.DOCUMENT:
            media_id, = struct.unpack("<q", buffer.read())

            return FileUniqueId(
                file_unique_type=file_unique_type,
                media_id=media_id
            )

        # TODO: Missing decoder for SECURE, ENCRYPTED and TEMP
        raise ValueError(f"Unknown decoder for file_unique_type {file_unique_type} of file_unique_id {file_unique_id}")

    def encode(self):
        if self.file_unique_type == FileUniqueType.WEB:
            string = struct.pack("<is", self.file_unique_type, String(self.url))
        elif self.file_unique_type == FileUniqueType.PHOTO:
            string = struct.pack("<iqi", self.file_unique_type, self.volume_id, self.local_id)
        elif self.file_unique_type == FileUniqueType.DOCUMENT:
            string = struct.pack("<iq", self.file_unique_type, self.media_id)
        else:
            # TODO: Missing encoder for SECURE, ENCRYPTED and TEMP
            raise ValueError(f"Unknown encoder for file_unique_type {self.file_unique_type}")

        return b64_encode(rle_encode(string))

    def __str__(self):
        return str({k: v for k, v in self.__dict__.items() if v is not None})
