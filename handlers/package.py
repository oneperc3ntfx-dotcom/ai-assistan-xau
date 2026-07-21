from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.package import package_keyboard


router = Router()



@router.callback_query(
lambda c:c.data=="activate"
)

async def activate(callback:CallbackQuery):


    await callback.message.answer(

"""
💎 <b>PILIH MEMBERSHIP</b>


Pilih paket AI Assistant Anda.


""",

reply_markup=package_keyboard()

)


    await callback.answer()
