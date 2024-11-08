from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from aiogram.utils.i18n import gettext as _, I18n

from bot.config import db

i18n = I18n(domain='messages', path='locales')

_ = i18n.gettext

dispatcher = Dispatcher()
dispatcher['i18n'] = i18n


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    if not (db.get('categories')):
        db['categories'] = {}
    if not db.get('products'):
        db['products'] = {}

    dispatcher['i18n'] = i18n

    command_list = [
        BotCommand(command='start', description=_('Botni ishga tushirish 🫡')),
        BotCommand(command='help', description=_('Yordam 📖')),
        BotCommand(command='language', description=_('Tilni almashtirish 🔄'))
    ]
    await bot.set_my_commands(command_list)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()
