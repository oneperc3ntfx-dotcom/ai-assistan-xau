from aiogram import Router
from aiogram.types import CallbackQuery, Message, FSInputFile

from aiogram.fsm.context import FSMContext

from states.payment import PaymentState

from keyboards.payment import payment_keyboard


from config import ADMIN_ID



router=Router()



@router.callback_query(
lambda c:c.data in ["1bulan","6bulan","12bulan"]
)

async def payment_page(
callback:CallbackQuery,
state:FSMContext
):


    await state.update_data(
        package=callback.data
    )


    await callback.message.answer_photo(

FSInputFile(
"assets/qris.jpg"
),

caption="""

💳 <b>AKTIVASI MEMBERSHIP</b>


Silakan lakukan pembayaran QRIS.


Setelah transfer klik tombol:


""",

reply_markup=payment_keyboard()

)


@router.callback_query(
lambda c:c.data=="transfer"
)

async def transfer(
callback:CallbackQuery,
state:FSMContext
):


    await state.set_state(
        PaymentState.photo
    )


    await callback.message.answer(

"""
Silakan upload bukti transfer.

"""
)

