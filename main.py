import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.commands import on_startup, on_shutdown
from bot.configs import TOKEN
from bot.starter import BEGIN_router

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    i18n = I18n(path='locales')
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(BEGIN_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
