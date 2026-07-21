from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def start_keyboard():


    return InlineKeyboardMarkup(
        inline_keyboard=[

            [

            InlineKeyboardButton(

            text="🤖 AKTIFKAN AI ASSISTANT",

            callback_data="activate"

            )

            ]

        ]
    )
