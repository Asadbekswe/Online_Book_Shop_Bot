from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from bot.config import db


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    if not (db.get('categories')):
        db['categories'] = {}
    if not db.get('products'):
        db['products'] = {}
    command_list = [
        BotCommand(command='start', description='Start the bot (botu başlat 🇹🇷)'),
        BotCommand(command='help', description='Help the bot (yardım 🇹🇷)'),
        BotCommand(command='language', description='Change language 🇺🇿 🔄 🇬🇧 🔄 🇹🇷')
    ]
    await bot.set_my_commands(command_list)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()
