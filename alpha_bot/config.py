class Config(object):
    LOGGER = True

    BOT_TOKEN = ""
    OWNER_ID = ""
    OWNER_USERNAME = ""

    WEBHOOK = False
    PORT = 8443
    URL = None
    DONATION_LINK = ""
    CERT_PATH = ""


class Release(Config):
    LOGGER = False


class Debug(Config):
    LOGGER = True
