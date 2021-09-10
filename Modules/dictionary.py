import urllib.parse

from requests import exceptions
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


def _parse_response_for_synonyms(r):
    synonyms = r.html.find('#synonyms-anchor > ul.mw-list', first=True)
    if not synonyms:
        return None

    keyboard_keys = synonyms.text.replace('\n', ' ').split(',')

    for k in keyboard_keys:
        if "[" in k:
            keyboard_keys.remove(k)

    if len(keyboard_keys) > 4:
        keyboard_keys = keyboard_keys[:4]

    return InlineKeyboardMarkup(_get_reply_keyboard(keyboard_keys))


def _parse_response_for_suggestions(r):
    suggestions = r.html.find('#left-content > div > p.spelling-suggestions')
    if not suggestions:
        return None

    if len(suggestions) > 10:
        suggestions = suggestions[:10]

    keyboard_keys = []
    for p in suggestions:
        keyboard_keys.append(p.text)

    return InlineKeyboardMarkup(_get_reply_keyboard(keyboard_keys))


def _parse_response_for_definition(r) -> str:
    definition = r.html.find('#dictionary-entry-1', first=True).text.replace("\n", "\n\n")
    return definition[:1000] + "..." if len(definition) > 1000 else definition


def _create_request(url: str):
    session = HTMLSession()

    try:
        r = session.get(url=url)
        return r
    except exceptions:
        return None


def _create_url(base_url: str, param: str) -> str:
    return urllib.parse.urljoin(base_url, urllib.parse.quote(param))


def _get_definition(word: str):
    base_url = "https://www.merriam-webster.com/dictionary/"
    url = _create_url(base_url=base_url, param=word)

    response = _create_request(url)
    if response is None:
        return None, None

    if response.status_code == 404:
        text = "Sorry, I am unable to find a valid result, but here are some suggestions to try again.\n\n"
        reply_markup = _parse_response_for_suggestions(response)

    else:
        text = _parse_response_for_definition(response)
        text += f"\n\nFor more info visit [here.]({url})"

        reply_markup = _parse_response_for_synonyms(response)

        if reply_markup is not None:
            text += f"\n\nBy the way, here are some synonyms."

    return text, reply_markup


def define_reply(update, _) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "cancel":
        query.edit_message_reply_markup()

    else:
        text, reply_markup = _get_definition(query.data)

        if text is None:
            text = "Sorry, There might be a problem."

        query.edit_message_text(text=text,
                                reply_markup=reply_markup,
                                disable_web_page_preview=True,
                                parse_mode=ParseMode.MARKDOWN)


def define(update, context) -> None:
    text, reply_markup = _get_definition(' '.join(context.args))

    if text is None:
        text = "Sorry, There might be a problem."

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=reply_markup,
                             disable_web_page_preview=True,
                             parse_mode=ParseMode.MARKDOWN)
