from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.config import db
from bot.config.conf import LINKS


def main_links_buttons() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for i in LINKS.keys():
        ikb.add(InlineKeyboardButton(text=i, url=LINKS[i]))
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


def admin_buttons() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='📚 Kitoblar')],
                  [KeyboardButton(text='Product ➕'), KeyboardButton(text='Category ➕')],
                  [KeyboardButton(text="Product ➖ (🗑 o'chirish)"), KeyboardButton(text="Category ➖ (🗑 o'chirish)")]],
        resize_keyboard=True)
    return rkb


def lang_commands():
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='Uz🇺🇿', callback_data='lang_uz'),
            InlineKeyboardButton(text='En🇺🇸', callback_data='lang_en'),
            InlineKeyboardButton(text='Tur🇹🇷', callback_data="lang_tur"),
            InlineKeyboardButton(text='Ru🇷🇺', callback_data='lang_ru'),
            InlineKeyboardButton(text='Ko🇰🇷', callback_data='lang_ko'))
    return ikb.as_markup()


def show_category(user_id):
    ikb = InlineKeyboardBuilder()

    if 'categories' not in db:
        db['categories'] = {}
    for k, v in db['categories'].items():
        ikb.add(InlineKeyboardButton(text=v, callback_data=k))
    ikb.add(InlineKeyboardButton(text=_('🔍 Qidirish'), switch_inline_query_current_chat=''))
    if 'baskets' not in db:
        db['baskets'] = {}
    if str(user_id) in db['baskets']:
        ikb.add(InlineKeyboardButton(text=f'🛒 Savat ({len(db["baskets"][str(user_id)])})', callback_data='savat'))
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


def make_plus_minus(quantity, product_id):
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="➖", callback_data="change-" + product_id),
            InlineKeyboardButton(text=str(quantity), callback_data="number"),
            InlineKeyboardButton(text="➕", callback_data="change+" + product_id)
            )
    ikb.row(InlineKeyboardButton(text=_("◀️Orqaga"), callback_data="categoryga"),
            InlineKeyboardButton(text=_('🛒 Savatga qo\'shish'), callback_data="savatga" + product_id + str(quantity)))
    return ikb


def main_buttons(**kwargs):
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_('📚 Kitoblar', **kwargs)))
    rkb.add(KeyboardButton(text=_('📃 Mening buyurtmalarim', **kwargs)))
    rkb.add(KeyboardButton(text=_("🔵 Biz ijtimoyi tarmoqlarda", **kwargs)))
    rkb.add(KeyboardButton(text=_('📞 Biz bilan bog\'lanish', **kwargs)))
    rkb.add(KeyboardButton(text=_('🌐 Tilni almshtirish', **kwargs)))
    rkb.adjust(1, 1, 2, repeat=True)
    return rkb.as_markup(resize_keyboard=True)
