from aiogram.types import *


def package_keyboard():


    return InlineKeyboardMarkup(
        inline_keyboard=[

[
InlineKeyboardButton(
text="🥇 1 Bulan Rp250.000",
callback_data="1bulan"
)
],


[
InlineKeyboardButton(
text="🥈 6 Bulan Rp500.000",
callback_data="6bulan"
)
],


[
InlineKeyboardButton(
text="🥉 12 Bulan Rp750.000",
callback_data="12bulan"
)
]

        ]
    )
