import base64url from "base64url";

export default class FileData {
    constructor(msgId, mimeType, size, name) {
        this.msgId = msgId;
        this.mimeType = mimeType;
        this.size = size;
        this.name = name;
    }

    // Encode fields into a compact Base64-encoded string
    encode() {
        const mimeBuffer = Buffer.alloc(20);
        mimeBuffer.write(this.mimeType, 'utf-8');

        const nameBuffer = Buffer.from(this.name, 'utf-8');

        // Calculate buffer size: 8 bytes for msgId and size, 20 bytes for mimeType, plus name length
        const buffer = Buffer.alloc(8 + mimeBuffer.length + nameBuffer.length);

        // Write `msgId` as a 4-byte integer
        buffer.writeUInt32LE(this.msgId, 0);

        // Write `size` as a 4-byte integer
        buffer.writeUInt32LE(this.size, 4);

        // Write `mimeType` into the fixed 20-byte space
        mimeBuffer.copy(buffer, 8);

        // Write `name` after `mimeType`
        nameBuffer.copy(buffer, 28);

        // Convert to URL-safe Base64
        return base64url.encode(buffer);
    }

    // Decode a Base64-encoded string into fields
    static decode(encodedString) {
        const buffer = base64url.toBuffer(encodedString);

        // Read `msgId` (4 bytes) and `size` (4 bytes)
        const msgId = buffer.readUInt32LE(0);
        const size = buffer.readUInt32LE(4);

        // Read `mimeType` (20 bytes, trimmed to remove extra nulls)
        const mimeType = buffer.toString('utf-8', 8, 28).replace(/\0/g, '');

        // Remaining buffer content is the `name`
        const name = buffer.toString('utf-8', 28);

        return new FileData(msgId, mimeType, size, name);
    }
}
