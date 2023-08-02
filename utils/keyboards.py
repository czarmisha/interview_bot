from telegram import InlineKeyboardButton

def agreement_keyboard():
    return [
        [
            InlineKeyboardButton("Да", callback_data=f"agreement_1"),
            InlineKeyboardButton("Нет", callback_data=f"agreement_0"),
        ],
        [InlineKeyboardButton(f"Отмена", callback_data='cancel')],
    ]

def final_keyboard():
    return [
        [
            InlineKeyboardButton("Да, хочу попробовать", callback_data=f"final_1"),
            InlineKeyboardButton("Нет, мне не подходит", callback_data=f"final_0"),
        ],
        [InlineKeyboardButton(f"Отмена", callback_data='cancel')],
    ]
