from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import db
from bot.keyboards import show_category, make_plus_minus, main_users_interface, change_language_command, \
    social_media_keyboards

main_router = Router()


@main_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    msg = _('Assalomu alaykum! Tanlovingiz 👇🏻.')
    if message.from_user.id not in db['users']:
        msg = _('Assalomu alaykum! \nXush kelibsiz!')
        users = db['users']
        users[str(message.from_user.id)] = True
        db['users'] = users
    await message.answer(text=msg, reply_markup=main_users_interface())


@main_router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer(_('''Buyruqlar:
/start - Botni ishga tushirish
/help - Yordam'''))


@main_router.message(F.text == __('🌐 Tilni almshtirish'))
async def change_language(message: Message) -> None:
    await message.answer(_('Tilni tanlang: '), reply_markup=change_language_command())


@main_router.message(Command(commands=['language']))
async def language_handler(message: Message) -> None:
    await change_language(message)


@main_router.callback_query(F.data.startswith('lang_'))
async def languages(callback: CallbackQuery, state: FSMContext) -> None:
    lang_code = callback.data.split('lang_')[-1]
    await state.update_data(locale=lang_code)
    if lang_code == 'uz':
        lang = _('Uzbek', locale=lang_code)
    elif lang_code == 'en':
        lang = _('Ingiliz', locale=lang_code)
    elif lang_code == "tur":
        lang = _('Turk', locale=lang_code)
    await callback.answer(_('{lang} tili tanlandi', locale=lang_code).format(lang=lang))
    msg = _('Assalomu alaykum! Tanlang.', locale=lang_code)
    await callback.message.answer(text=msg, reply_markup=main_users_interface(locale=lang_code))


@main_router.message(F.text == __("🔵 Biz ijtimoyi tarmoqlarda"))
async def our_social_network(message: Message) -> None:
    await message.answer('Biz ijtimoiy tarmoqlarda', reply_markup=social_media_keyboards())


@main_router.message(F.text == __('📚 Kitoblar'))
async def books(message: Message) -> None:
    await message.answer(_('Kategoriyalardan birini tanlang'), reply_markup=show_category(message.from_user.id))


@main_router.callback_query(F.data.startswith('orqaga'))
async def back_handler(callback: CallbackQuery):
    await callback.message.edit_text(_('Categoriyalardan birini tanlang'),
                                     reply_markup=show_category(callback.from_user.id))


@main_router.message(F.text == __("📞 Biz bilan bog'lanish"))
async def message(message: Message) -> None:
    text = _("""\n
\n
Telegram: @Mexmonjonovuz\n
📞  +{number}\n
🤖 Bot Mexmonjonov Asadbek @Mexmonjonovuz tomonidan tayorlandi.\n""".format(number=998901209552))
    await message.answer(text=text, parse_mode=ParseMode.HTML)


@main_router.message(lambda msg: msg.text[-36:] in db['products'])
async def answer_inline_query(message: Message):
    msg = message.text[-36:]
    product = db['products'][msg]
    ikb = make_plus_minus(1, msg)
    await message.delete()
    await message.answer_photo(photo=product['image'], caption=product['text'], reply_markup=ikb.as_markup())


@main_router.callback_query()
async def product_handler(callback: CallbackQuery):
    if callback.data in db['categories']:
        ikb = InlineKeyboardBuilder()
        for k, val in db['products'].items():
            if val['category_id'] == callback.data:
                ikb.add(InlineKeyboardButton(text=val['name'], callback_data=k))
        if str(callback.from_user.id) in db['baskets']:
            ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(db["baskets"][str(callback.from_user.id)])})',
                                         callback_data='savat'))
        ikb.add(InlineKeyboardButton(text=_("◀️ orqaga"), callback_data='orqaga'))
        ikb.adjust(2, repeat=True)
        await callback.message.edit_text(db['categories'][callback.data], reply_markup=ikb.as_markup())
    elif callback.data in db['products']:
        product = db['products'][callback.data]
        ikb = make_plus_minus(1, callback.data)
        await callback.message.delete()
        await callback.message.answer_photo(photo=product['image'], caption=product['text'],
                                            reply_markup=ikb.as_markup())
