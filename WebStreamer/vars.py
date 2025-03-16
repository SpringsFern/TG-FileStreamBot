# This file is a part of TG-FileStreamBot
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Var(object):
    MULTI_CLIENT = False
    API_ID = int(environ.get("API_ID"))
    API_HASH = str(environ.get("API_HASH"))
    BIN_CHANNEL = int(
        environ.get("BIN_CHANNEL", None)
    )  # you NEED to use a CHANNEL when you're using MULTI_CLIENT
    BOT_TOKEN = str(environ.get("BOT_TOKEN"))

    ALLOWED_USERS = [x.strip("@ ") for x in str(environ.get("ALLOWED_USERS", "") or "").split(",") if x.strip("@ ")]
    BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
    CHUNK_SIZE: int = int(environ.get("CHUNK_SIZE", 1024 * 1024)) #bytes
    CONNECTION_LIMIT = int(environ.get("CONNECTION_LIMIT", 20))
    CUSTOM_URL:str = environ.get("CUSTOM_URL", None)
    DEBUG: bool = str(environ.get("DEBUG", "0").lower()) in ("1", "true", "t", "yes", "y")
    FQDN = str(environ.get("FQDN", BIND_ADDRESS))
    HAS_SSL = str(environ.get("HAS_SSL", "0").lower()) in ("1", "true", "t", "yes", "y")
    KEEP_ALIVE = str(environ.get("KEEP_ALIVE", "0").lower()) in  ("1", "true", "t", "yes", "y")
    LINK_TEMPLATE:str = environ.get("LINK_TEMPLATE", "{url}/dl/{id}/{name}")
    NO_PORT = str(environ.get("NO_PORT", "0").lower()) in ("1", "true", "t", "yes", "y")
    NO_UPDATE = str(environ.get("NO_UPDATE", "0").lower()) in ("1", "true", "t", "yes", "y")
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "600"))  # 10 minutes
    PORT = int(environ.get("PORT", 8080))
    REQUEST_LIMIT = int(environ.get("REQUEST_LIMIT", 5))
    SLEEP_THRESHOLD = int(environ.get("SLEEP_THRESHOLD", "60"))  # 1 minte
    TRUST_HEADERS: bool = str(environ.get("TRUST_HEADERS", "1").lower()) in ("1", "true", "t", "yes", "y")
    UPDATES_CHANNEL = str(environ.get('UPDATES_CHANNEL', "Telegram"))
    URL = f"http{"s" if HAS_SSL else ""}://{FQDN}{"" if NO_PORT else ":" + str(PORT)}/"
