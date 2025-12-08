import asyncio
from aiogram import Dispatcher

from app.bot import bot, dp

# Handlers
from app.handlers.start import start_router
from app.handlers.chat import chat_router
from app.handlers.admin import admin_router


async def main():
    # Barcha handler routerlarini ulaymiz
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(chat_router)

    print("🤖 Zaytra AI Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())