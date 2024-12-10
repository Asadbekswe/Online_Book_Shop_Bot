import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot.config import TOKEN
from bot.utils.starter import router
from db import database

dp = Dispatcher()


async def on_startup(bot: Bot):
    # await database.drop_all()
    await database.create_all()
    command_list = [
        BotCommand(command='start', description='Start the bot 🫡'),
        BotCommand(command='help', description='Help 📖'),
        BotCommand(command='language', description='Change language 🔄')
    ]
    await bot.set_my_commands(command_list)


async def on_shutdown(bot: Bot):
    await bot.delete_my_commands()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    i18n = I18n(path="locales")
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
