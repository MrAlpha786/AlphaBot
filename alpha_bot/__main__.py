import importlib

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from alpha_bot import dispatcher, updater, WEBHOOK, URL, PORT, BOT_TOKEN, CERT_PATH, LOGGER
from alpha_bot.modules import MODULES
from alpha_bot.modules.utils.keyboard import get_keyboard_markup

HELP_STRINGS = {}

__help_str__ = """
Hello! my name is *{}*.

*Main* available commands:
 - /start: Start the bot...
 - /help: help....
 - /donate: To find out more about donating!

And the following:
""".format(dispatcher.bot.first_name)

for module in MODULES:
    imported_mod = importlib.import_module("alpha_bot.modules." + module)
    if not hasattr(imported_mod, "__mod_name__"):
        imported_mod.__mod_name__ = imported_mod.__name__

    if hasattr(imported_mod, "__help_str__"):
        HELP_STRINGS[imported_mod.__mod_name__] = imported_mod.__help_str__
    else:
        HELP_STRINGS[imported_mod.__mod_name__] = "Sorry! No help is available for this module."


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi {update.effective_chat.full_name}, I am *{dispatcher.bot.first_name}*.",
                             parse_mode=ParseMode.MARKDOWN)


def help_reply(update: Update, _) -> None:
    query = update.callback_query
    query.answer()

    if query.data == "help_back":
        query.edit_message_text(text=__help_str__,
                                reply_markup=get_keyboard_markup(list(HELP_STRINGS.keys()),
                                                                 prefix="help"),
                                parse_mode=ParseMode.MARKDOWN)

    else:
        query.edit_message_text(text=HELP_STRINGS[query.data[5:]],
                                reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(text="Back",
                                                           callback_data="help_back")]]),
                                parse_mode=ParseMode.MARKDOWN)


def help_me(update: Update, context: CallbackContext) -> None:
    reply_markup = get_keyboard_markup(list(HELP_STRINGS.keys()),
                                       prefix="help")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=__help_str__,
                             reply_markup=reply_markup,
                             parse_mode=ParseMode.MARKDOWN)


def unknown(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Sorry, I don\'t understand the command.\n'
                                  'Type /help for a list of valid commands.')


def main() -> None:
    """Run bot."""

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_me))
    dispatcher.add_handler(CallbackQueryHandler(help_reply, pattern=r"help_"))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=BOT_TOKEN,
                              webhook_url=URL + BOT_TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + BOT_TOKEN,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + BOT_TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(MODULES))
    main()
