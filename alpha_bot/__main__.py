import logging
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from alpha_bot import Modules

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi {update.effective_chat.full_name}, I am AlphaBot.")


def help_me(update: Update, context: CallbackContext) -> None:
    help_text = f"You can use the commands listed below:\n\n" \
                f"/help - To display this message.\n" \
                f"/yell <Message> - To yell a message.\n" \
                f"/define <Word> - Get meaning of a word or phrase."
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=help_text)


def yell(update: Update, context: CallbackContext) -> None:
    text_yell = ' '.join(context.args).upper()
    text_yell = text_yell.replace('A', 'AAA') \
        .replace('E', 'EEE') \
        .replace('I', 'III') \
        .replace('O', 'OOO') \
        .replace('U', 'UUU')
    text_yell += text_yell[-1] * 5 + '!'
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text_yell)


def echo(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


def unknown(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Sorry, I don\'t understand the command.\n'
                                  'Type /help for a list of valid commands.')


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_me))
    dispatcher.add_handler(CommandHandler('yell', yell))
    dispatcher.add_handler(CommandHandler('define', Modules.define))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.dispatcher.add_handler(CallbackQueryHandler(Modules.define_reply))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
