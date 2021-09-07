import urllib.parse

from requests_html import HTMLSession
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup


def _get_reply_keyboard(keys: list) -> list:
    keyboard = []
    row = []
    for k in keys:
        if len(row) == 2:
            keyboard.append(row)
            row = []
        row.append(InlineKeyboardButton(text=k, callback_data=k))
    keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="Cancel", callback_data="cancel")])

    return keyboard


def _show_spelling_suggestions(elements: list) -> tuple:
    if len(elements) > 10:
        elements = elements[:10]

    keyboard_keys = []
    for p in elements:
        keyboard_keys.append(p.text)

    reply_markup = InlineKeyboardMarkup(_get_reply_keyboard(keyboard_keys))
    response = "Sorry, I am unable to find a valid result, but here are some suggestions to try again.\n\n"

    return response, reply_markup


def _show_synonyms(element) -> InlineKeyboardMarkup:
    keyboard_keys = element.text.replace('\n', ' ').split(',')

    for k in keyboard_keys:
        if "[" in k:
            keyboard_keys.remove(k)

    if len(keyboard_keys) > 4:
        keyboard_keys = keyboard_keys[:4]

    return InlineKeyboardMarkup(_get_reply_keyboard(keyboard_keys))


def search_merriam_webster(word: str) -> tuple:
    base_url = "https://www.merriam-webster.com/dictionary/"
    url = urllib.parse.urljoin(base_url, urllib.parse.quote(word))
    session = HTMLSession()

    try:
        r = session.get(url=url)

        if r.status_code == 404:
            suggestions = r.html.find('#left-content > div > p.spelling-suggestions')
            if not suggestions:
                return None, None
            return _show_spelling_suggestions(suggestions)

        r.raise_for_status()
    except IOError:
        return None, None

    response = r.html.find('#dictionary-entry-1', first=True).text.replace("\n", "\n\n")
    response += f"\n\nFor more info visit [here.]({url})"

    synonyms = r.html.find('#synonyms-anchor > ul.mw-list', first=True)
    if not synonyms:
        return response, None

    reply_markup = _show_synonyms(synonyms)
    response += f"\n\nBy the way, here are some synonyms."

    return response, reply_markup


def define_reply(update, _) -> None:
    query = update.callback_query
    query.answer()
    if not query.data == "cancel":
        response, reply_markup = search_merriam_webster(query.data)
        if not response:
            response = "Sorry, There might be a problem."
        query.edit_message_text(text=response,
                                reply_markup=reply_markup,
                                disable_web_page_preview=True,
                                parse_mode=ParseMode.MARKDOWN)
    else:
        query.edit_message_reply_markup()


def define(update, context) -> None:
    response, reply_markup = search_merriam_webster(' '.join(context.args))

    if response is None:
        response = "Sorry, There might be a problem."

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response,
                             reply_markup=reply_markup,
                             disable_web_page_preview=True,
                             parse_mode=ParseMode.MARKDOWN)
