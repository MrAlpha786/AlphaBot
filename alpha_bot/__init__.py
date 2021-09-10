import logging
import os
import sys

from telegram.ext import Updater

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    LOGGER.error("You MUST have a python version of at least 3.7! Multiple features depend on this. Bot quitting.")
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
    OWNER_ID = int(os.environ.get('OWNER_ID'))
    OWNER_USERNAME = os.environ.get('OWNER_USERNAME')

    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    DONATION_LINK = os.environ.get('DONATION_LINK')

else:
    from alpha_bot.config import Debug as Config

    BOT_TOKEN = Config.BOT_TOKEN
    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    OWNER_USERNAME = Config.OWNER_USERNAME

    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH

    DONATION_LINK = Config.DONATION_LINK

updater = Updater(BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher
