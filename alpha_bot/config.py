class Config(object):
    LOGGER = True

    BOT_TOKEN = ""
    OWNER_ID = "587454251"
    OWNER_USERNAME = "MrAlpha786"

    WEBHOOK = False
    PORT = 8443
    URL = None
    DONATION_LINK = ""
    CERT_PATH = ""


class Release(Config):
    LOGGER = False


class Debug(Config):
    LOGGER = True
