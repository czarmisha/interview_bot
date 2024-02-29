from telegram import InlineKeyboardButton
from text.start import text


def lang_keyboard():
    return [
        [
            InlineKeyboardButton("🇺🇿", callback_data=f"lang_uz"),
            InlineKeyboardButton("🇷🇺", callback_data=f"lang_ru"),
            InlineKeyboardButton("🇺🇸", callback_data=f"lang_en"),
        ]
    ]

def agreement_keyboard(lang='ru'):
    return [
        [
            InlineKeyboardButton(text['yes'][lang], callback_data=f"agreement_1"),
            InlineKeyboardButton(text['no'][lang], callback_data=f"agreement_0"),
        ],
        [InlineKeyboardButton(text['cancel'][lang], callback_data='cancel')],
    ]

def final_keyboard(lang='ru'):
    return [
        [
            InlineKeyboardButton(text['want_try'][lang], callback_data=f"final_1"),
            InlineKeyboardButton(text['!want_try'][lang], callback_data=f"final_0"),
        ],
        [InlineKeyboardButton(text['cancel'][lang], callback_data='cancel')],
    ]

def statistic_keyboard(lang='ru'):
    return [
        [InlineKeyboardButton("За сегодня", callback_data=f"type_1")],
        [InlineKeyboardButton("За вчера", callback_data=f"type_2")],
        [InlineKeyboardButton("За текущую неделю", callback_data=f"type_3")],
        [InlineKeyboardButton("За прошлую неделю", callback_data=f"type_4")],
        [InlineKeyboardButton("За текущий месяц", callback_data=f"type_5")],
        [InlineKeyboardButton("За прошлый месяц", callback_data=f"type_6")],
        # [InlineKeyboardButton("За конкретный месяц", callback_data=f"type_7")],
        # [InlineKeyboardButton("За конкретную дату", callback_data=f"type_8")],
        [InlineKeyboardButton("За все время", callback_data=f"type_9")],
        [InlineKeyboardButton(text['cancel'][lang], callback_data='cancel')],
    ]
