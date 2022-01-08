import mimetypes
mimetypes.init()

def mimetype(filename):
    mimestart = mimetypes.guess_type(filename)[0]

    if mimestart != None:
        mimestart = mimestart.split('/')[0]

        return mimestart