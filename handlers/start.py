from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from keyboards.start import start_keyboard


router = Router()



@router.message(CommandStart())
async def start(message: Message):


    photo = FSInputFile(
        "assets/welcome.jpg"
    )


    name = message.from_user.first_name


    text=f"""

🤖 <b>XAU AI Assistant</b>


Halo <b>{name}</b> 👋


Selamat datang di XAU AI Assistant.

"contoh AI ASSISTANT pada gambar diatas"


Dapatkan AI ASSISTANT XAU,
market update, dan informasi trading
langsung melalui Telegram pribadi.


━━━━━━━━━━━━━━


<b>Member mendapatkan:</b>


📈 XAUUSD Analysis

🧠 Smart Money Concept

⚡ Update Trading


━━━━━━━━━━━━━━


Aktifkan AI Assistant Anda.


"""


    await message.answer_photo(

        photo=photo,

        caption=text,

        reply_markup=start_keyboard()

    )
