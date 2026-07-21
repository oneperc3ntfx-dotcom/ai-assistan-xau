from aiogram.types import *


def payment_keyboard():

    return InlineKeyboardMarkup(

inline_keyboard=[

[
InlineKeyboardButton(

text="✅ SAYA SUDAH TRANSFER",

callback_data="transfer"

)
]

]

)
