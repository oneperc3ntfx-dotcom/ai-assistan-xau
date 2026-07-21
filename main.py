import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties


from config import BOT_TOKEN

from handlers import start
from handlers import package
from handlers import payment
from handlers import admin


async def main():

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode="HTML"
        )
    )


    dp = Dispatcher()


    dp.include_router(start.router)
    dp.include_router(package.router)
    dp.include_router(payment.router)
    dp.include_router(admin.router)


    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
