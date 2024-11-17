import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.config import TOKEN
from bot.handlers.commands import on_startup, on_shutdown
from bot.utils.starter import router

dp = Dispatcher()

locales_path = f"{os.getcwd()}/locales"


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    i18n = I18n(path=locales_path)
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
