import asyncio

from aiogram import Dispatcher

from app.core.bot_factory import create_bot
from app.core.logging import setup_logging
from app.config.settings import Settings
from app.db.sqlite import init_db
from app.routers import user_router, admin_router


async def main():


    setup_logging()
    settings = Settings()

    bot = create_bot(settings.BOT_TOKEN)
    dp = Dispatcher()

    # Инициализация БД
    await init_db(settings.DB_PATH)

    # Роутеры
    dp.include_router(user_router)
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, settings=settings)


if __name__ == "__main__":
    asyncio.run(main())