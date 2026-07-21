import asyncio

from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F

from aiogram.filters import CommandStart

from aiogram.types import (
    Message,
    CallbackQuery,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


from config import (
    BOT_TOKEN,
    PAYMENT_GROUP_ID,
    SIGNAL_BOT
)


from packages import PACKAGE_MAP

from apps_script import save_member



bot = Bot(
    token=BOT_TOKEN
)


dp = Dispatcher()



# penyimpanan sementara
user_packages = {}

user_proofs = {}



# ==========================
# START WELCOME
# ==========================


@dp.message(CommandStart())
async def start(message: Message):


    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

            InlineKeyboardButton(

                text="🤖 AKTIFKAN AI ASSISTANT",

                callback_data="activate"

            )

            ]

        ]

    )


    photo = FSInputFile(
        "assets/ai_example.jpg"
    )



    text = f"""

🤖 <b>XAU AI Assistant</b>


Halo <b>{message.from_user.first_name}</b> 👋


Di atas adalah contoh tampilan
AI Assistant yang akan Anda dapatkan.


AI Assistant akan membantu Anda mendapatkan
informasi dan analisa XAUUSD langsung
melalui Telegram pribadi Anda.


━━━━━━━━━━━━━━


<b>Yang Anda dapatkan:</b>


📈 Analisa XAUUSD

🧠 Smart Money Concept Analysis

📰 Update Market & News

⚡ Informasi Trading Terbaru

🤖 AI Assistant Pribadi


━━━━━━━━━━━━━━


Tidak perlu mencari signal di grup.

Tidak perlu membaca chat yang menumpuk.


Semua informasi akan dikirim langsung
melalui AI Assistant pribadi Anda.


Klik tombol di bawah untuk mengaktifkan.


"""


    await message.answer_photo(

        photo=photo,

        caption=text,

        reply_markup=keyboard,

        parse_mode="HTML"

    )





# ==========================
# PILIH PACKAGE
# ==========================


@dp.callback_query(
    F.data=="activate"
)

async def choose_package(
    callback: CallbackQuery
):


    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[


            [

            InlineKeyboardButton(

                text="🥇 1 Bulan • Rp250.000",

                callback_data="pkg_1month"

            )

            ],


            [

            InlineKeyboardButton(

                text="🥈 6 Bulan • Rp500.000",

                callback_data="pkg_6month"

            )

            ],


            [

            InlineKeyboardButton(

                text="🥉 12 Bulan • Rp850.000",

                callback_data="pkg_12month"

            )

            ],


            [

            InlineKeyboardButton(

                text="👑 Permanent • Rp1.500.000",

                callback_data="pkg_permanent"

            )

            ]

        ]

    )


    await callback.message.answer(

"""

💎 <b>PILIH MEMBERSHIP</b>


Pilih durasi akses
XAU AI Assistant Anda.


━━━━━━━━━━━━━━


🥇 1 Bulan
Rp250.000


🥈 6 Bulan
Rp500.000


🥉 12 Bulan
Rp850.000


👑 Permanent
Rp1.500.000


━━━━━━━━━━━━━━


Silakan pilih paket.


""",

reply_markup=keyboard,

parse_mode="HTML"

)


    await callback.answer()





# ==========================
# QRIS
# ==========================


@dp.callback_query(
F.data.startswith("pkg_")
)

async def show_payment(
callback: CallbackQuery
):


    package_key = callback.data.replace(
        "pkg_",
        ""
    )


    user_packages[
        callback.from_user.id
    ] = package_key



    data = PACKAGE_MAP[package_key]



    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

            InlineKeyboardButton(

                text="📸 UPLOAD BUKTI PEMBAYARAN",

                callback_data="upload"

            )

            ]

        ]

    )



    await callback.message.answer_photo(

        photo=FSInputFile(
            "assets/qris.jpg"
        ),


        caption=f"""

💳 <b>AKTIVASI MEMBERSHIP</b>


Paket:

<b>{data['label']}</b>


Biaya:

<b>Rp {data['price']:,}</b>


━━━━━━━━━━━━━━


Silakan lakukan pembayaran
melalui QRIS di atas.


Setelah pembayaran selesai,
upload bukti pembayaran Anda.


Admin akan melakukan verifikasi
dan mengaktifkan AI Assistant Anda.


""",

reply_markup=keyboard,

parse_mode="HTML"

)


    await callback.answer()





# ==========================
# MINTA UPLOAD
# ==========================


@dp.callback_query(
F.data=="upload"
)

async def upload_request(
callback:CallbackQuery
):


    await callback.message.answer(

"""

Silakan kirim screenshot
atau foto bukti pembayaran.


"""

)


    await callback.answer()





# ==========================
# TERIMA BUKTI
# ==========================


@dp.message(
F.photo
)

async def receive_payment(
message: Message
):


    user_proofs[
        message.from_user.id
    ] = message.photo[-1].file_id



    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

            InlineKeyboardButton(

                text="✅ KIRIM VERIFIKASI",

                callback_data="verify"

            )

            ]

        ]

    )



    await message.answer(

"""

✅ Bukti pembayaran diterima.


Klik tombol di bawah untuk
mengirim permintaan verifikasi Admin.


""",

reply_markup=keyboard,

parse_mode="HTML"

)






# ==========================
# KIRIM ADMIN
# ==========================


@dp.callback_query(
F.data=="verify"
)

async def verify(
callback:CallbackQuery
):


    user_id = callback.from_user.id


    package_key = user_packages.get(
        user_id
    )


    proof = user_proofs.get(
        user_id
    )


    if not package_key or not proof:

        await callback.answer(
            "Data belum lengkap",
            show_alert=True
        )

        return



    data = PACKAGE_MAP[package_key]



    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

            InlineKeyboardButton(

                text="✅ APPROVE",

                callback_data=f"approve_{user_id}"

            ),


            InlineKeyboardButton(

                text="❌ REJECT",

                callback_data=f"reject_{user_id}"

            )

            ]

        ]

    )



    await bot.send_photo(

        chat_id=PAYMENT_GROUP_ID,

        photo=proof,

        caption=f"""

📥 <b>PAYMENT VERIFICATION</b>


Nama:
{callback.from_user.full_name}


Username:
@{callback.from_user.username}


Telegram ID:
<code>{user_id}</code>


Paket:

{data['label']}


Harga:

Rp {data['price']:,}


""",

reply_markup=keyboard,

parse_mode="HTML"

)



    await callback.message.answer(

        "⏳ Pembayaran sedang diverifikasi Admin."

    )


    await callback.answer()





# ==========================
# APPROVE
# ==========================


@dp.callback_query(
F.data.startswith("approve_")
)

async def approve(
callback:CallbackQuery
):


    user_id = int(
        callback.data.split("_")[1]
    )



    user = await bot.get_chat(
        user_id
    )



    package_key = user_packages[user_id]


    data = PACKAGE_MAP[package_key]



    if data["days"] == 9999:

        expired = "PERMANENT"


    else:

        expired = (

            datetime.now()

            +

            timedelta(
                days=data["days"]
            )

        ).strftime("%d-%m-%Y")



    save_member({

        "telegram_id":user_id,

        "username":user.username or "",

        "nama":user.full_name,

        "paket":data["label"],

        "harga":data["price"],

        "register":
        datetime.now().strftime("%d-%m-%Y"),

        "expired":expired,

        "status":"ACTIVE"

    })



    button = InlineKeyboardMarkup(

        inline_keyboard=[

            [

            InlineKeyboardButton(

                text="🤖 BUKA AI ASSISTANT",

                url=SIGNAL_BOT

            )

            ]

        ]

    )



    await bot.send_message(

        user_id,


f"""

🎉 <b>MEMBERSHIP BERHASIL DIAKTIFKAN</b>


Terima kasih telah bergabung.


━━━━━━━━━━━━━━


📦 Paket:

<b>{data['label']}</b>


⏳ Berlaku sampai:

<b>{expired}</b>


━━━━━━━━━━━━━━


AI Assistant Anda sudah aktif.


Klik tombol di bawah untuk mulai menggunakan.


""",

reply_markup=button,

parse_mode="HTML"

)



    await callback.message.answer(
        "✅ Member berhasil diaktifkan."
    )



# ==========================
# REJECT
# ==========================


@dp.callback_query(
F.data.startswith("reject_")
)

async def reject(
callback:CallbackQuery
):


    user_id = int(
        callback.data.split("_")[1]
    )


    await bot.send_message(

        user_id,

"""

❌ Pembayaran belum dapat diverifikasi.


Silakan hubungi Admin.

"""

    )


    await callback.answer()





# ==========================
# RUN
# ==========================


async def main():

    print(
        "XAU Welcome Bot Running..."
    )


    await dp.start_polling(
        bot
    )



if __name__=="__main__":

    asyncio.run(main())
