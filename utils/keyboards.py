from telegram import InlineKeyboardButton

def agreement_keyboard():
    return [
        [
            InlineKeyboardButton("Да", callback_data=f"agreement_1"),
            InlineKeyboardButton("Нет", callback_data=f"agreement_0"),
        ],
        [InlineKeyboardButton(f"Отмена", callback_data='cancel')],
    ]

def about_keyboard():
    return [
        [
            InlineKeyboardButton("Да", callback_data=f"about_1"),
            InlineKeyboardButton("Нет", callback_data=f"about_0"),
        ],
        [InlineKeyboardButton(f"Отмена", callback_data='cancel')],
    ]