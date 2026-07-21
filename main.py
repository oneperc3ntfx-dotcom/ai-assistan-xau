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

from spreadsheet import save_member



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

<b>🤖 XAU AI ASSISTANT PREMIUM</b>


Halo <b>{message.from_user.first_name}</b> 👋


Selamat datang di layanan
<b>XAU AI Assistant Premium</b>.


━━━━━━━━━━━━━━━━━━


<b>🚀 Apa yang Anda dapatkan?</b>


📈 <b>Analisa XAUUSD Premium</b>

🧠 <b>Smart Money Concept Analysis</b>

📰 <b>Market News Berdampak Tinggi</b>

⚡ <b>Update Pergerakan Gold Terbaru</b>

🤖 <b>AI Assistant Pribadi Telegram</b>


━━━━━━━━━━━━━━━━━━


<b>Kenapa berbeda dari grup signal biasa?</b>


Anda tidak perlu lagi:

❌ Membaca chat yang menumpuk

❌ Mencari pesan penting

❌ Takut melewatkan momentum market


Semua informasi penting akan dikirim
langsung melalui <b>AI Assistant pribadi Anda</b>.


━━━━━━━━━━━━━━━━━━


<b>Aktifkan akses Anda sekarang</b>


Dapatkan bantuan AI untuk membantu
menganalisa market Gold secara lebih cepat
dan terstruktur.


Klik tombol di bawah untuk memulai
proses aktivasi membership.


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

<b>💎 PILIH MEMBERSHIP
XAU AI ASSISTANT</b>


Pilih paket akses sesuai kebutuhan
Anda untuk mendapatkan layanan
AI Assistant Premium.


━━━━━━━━━━━━━━━━━━


🥇 <b>1 Bulan</b>

💰 Rp250.000


🥈 <b>6 Bulan</b>

💰 Rp500.000


🥉 <b>12 Bulan</b>

💰 Rp850.000


👑 <b>Permanent Access</b>

💰 Rp1.500.000


━━━━━━━━━━━━━━━━━━


✨ Semua paket mendapatkan akses
AI Assistant Telegram pribadi.


Silakan pilih paket untuk melanjutkan
proses aktivasi.


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



    await callback.message.answer_photo(

        photo=FSInputFile(
            "assets/qris.jpg"
        ),


        caption=f"""

<b>💳 AKTIVASI MEMBERSHIP
XAU AI ASSISTANT</b>


📦 <b>Paket Dipilih:</b>

{data['label']}


💰 <b>Total Pembayaran:</b>

Rp {data['price']:,}


━━━━━━━━━━━━━━━━━━


Silakan lakukan pembayaran
melalui QRIS di atas.


Setelah pembayaran selesai:


📸 Kirim screenshot atau foto
<b>bukti pembayaran</b> ke chat ini.


Admin akan melakukan pengecekan
dan mengaktifkan akses Anda.


━━━━━━━━━━━━━━━━━━


Terima kasih telah mempercayakan
akses market intelligence Anda
bersama <b>XAU AI Assistant</b>.


""",

        parse_mode="HTML"

    )







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

<b>📸 UPLOAD BUKTI PEMBAYARAN</b>


Silakan kirim screenshot atau foto
bukti pembayaran QRIS Anda.


Pastikan gambar terlihat jelas agar
proses verifikasi dapat dilakukan
dengan cepat.


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

<b>✅ BUKTI PEMBAYARAN DITERIMA</b>


Bukti pembayaran berhasil diterima.


Silakan klik tombol di bawah untuk
mengirim permintaan verifikasi
kepada Admin.


⏳ Proses pengecekan dilakukan
setelah Admin menerima laporan.


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

<b>📥 PAYMENT VERIFICATION</b>


━━━━━━━━━━━━━━━━━━


👤 <b>Nama:</b>

{callback.from_user.full_name}


🔹 <b>Username:</b>

@{callback.from_user.username}


🆔 <b>Telegram ID:</b>

<code>{user_id}</code>


📦 <b>Paket:</b>

{data['label']}


💰 <b>Total:</b>

Rp {data['price']:,}


━━━━━━━━━━━━━━━━━━


Silakan lakukan pengecekan
dan pilih tindakan.


""",

        reply_markup=keyboard,

        parse_mode="HTML"

    )



    await callback.message.answer(

        """

<b>⏳ PEMBAYARAN DALAM PROSES VERIFIKASI</b>


Bukti pembayaran telah dikirim
kepada Admin.


Mohon tunggu proses pengecekan.


Terima kasih atas kesabaran Anda.


"""

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

<b>🎉 MEMBERSHIP AKTIF</b>


Selamat! Pembayaran Anda telah
berhasil diverifikasi.


━━━━━━━━━━━━━━━━━━


📦 <b>Paket:</b>

{data['label']}


⏳ <b>Masa Aktif:</b>

{expired}


━━━━━━━━━━━━━━━━━━


🤖 AI Assistant Anda sudah aktif.


Klik tombol di bawah untuk mulai
menggunakan layanan premium.


Terima kasih telah menjadi bagian
dari <b>XAU AI Assistant</b>.


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

<b>❌ PEMBAYARAN BELUM DAPAT
DIVERIFIKASI</b>


Mohon maaf, pembayaran Anda
belum dapat kami verifikasi.


Silakan hubungi Admin untuk
informasi lebih lanjut.


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
