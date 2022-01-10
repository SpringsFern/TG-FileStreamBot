import mimetypes
import urllib.parse

# def mimetype(filename):
#     mimetypes.init()
#     mimestart = mimetypes.guess_type(filename)[0]

#     if mimestart != None:
#         mimestart = mimestart.split('/')[0]

#         return mimestart
#     else:
#         return "None"

def get_media_file_name(m):
    media = m.video or m.document or m.audio
    if media and media.file_name:
        return media.file_name
        # return urllib.parse.quote_plus(media.file_name)
    else:
        return "None"

def get_media_file_size(m):
    media = m.video or m.audio or m.document
    if media and media.file_size:
        return media.file_size
    else:
        return "None"

def get_media_mime_type(m):
    media = m.video or m.audio or m.document
    if media and media.mime_type:
        # mime_type=media.mime_type.split('/')[0]
        mimetype=media.mime_type
        return mimetype
    else:
        return "None/unknown"