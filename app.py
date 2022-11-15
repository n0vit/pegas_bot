import asyncio
import logging

from aiogram import Bot, Dispatcher

from tgbot.handlers.admin.adds import router_group
from tgbot.handlers.admin.admin import router as admin_router
from tgbot.loader import config, logger, scheduler


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.debug("Strating")

    bot = Bot(token=config.tg_bot.token, parse_mode="html")
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(router_group)
    scheduler.start()

    # start
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
