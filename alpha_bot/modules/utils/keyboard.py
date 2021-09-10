from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard_markup(buttons: list, prefix: str) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    for b in buttons:
        if len(row) == 2:
            keyboard.append(row)
            row = []
        else:
            row.append(InlineKeyboardButton(text=b, callback_data=prefix + "_" + b))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)
