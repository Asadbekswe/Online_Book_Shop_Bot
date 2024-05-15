from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.config import db

SOCIAL_LINKS = ['https://t.me/ikar_factor', 'https://t.me/factor_books', 'https://t.me/factorbooks']
SOCIAL_TEXT_BUTTONS = ['IKAR | Factor Books', 'Factor Books', '\"Factor Books\" nashiryoti']


def social_media_keyboards() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    for i in range(max(len(SOCIAL_LINKS), len(SOCIAL_TEXT_BUTTONS))):
        ikb.add(InlineKeyboardButton(text=SOCIAL_TEXT_BUTTONS[i], url=SOCIAL_LINKS[i]))
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


def admins_for_interface() -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Product+'), KeyboardButton(text='Category+')],
                  [KeyboardButton(text='delete product'), KeyboardButton(text='delete category')],
                  [KeyboardButton(text='📚 Kitoblar')]
                  ],
        resize_keyboard=True)
    return rkb


def change_language_command():
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text='Uz🇺🇿', callback_data='lang_uz'),
            InlineKeyboardButton(text='En🇬🇧', callback_data='lang_en'),
            InlineKeyboardButton(text='Tur🇹🇷', callback_data="lang_tur"))
    return ikb.as_markup()


def show_category(user_id):
    ikb = InlineKeyboardBuilder()
    for k, v in db['categories'].items():
        ikb.add(InlineKeyboardButton(text=v, callback_data=k))
    ikb.add(InlineKeyboardButton(text=_('🔍 Qidirish'), switch_inline_query_current_chat=''))
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


def main_users_interface(**kwargs):
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text=_('📚 Kitoblar', **kwargs)))
    rkb.add(KeyboardButton(text=_('📃 Mening buyurtmalarim', **kwargs)))
    rkb.add(KeyboardButton(text=_("🔵 Biz ijtimoyi tarmoqlarda", **kwargs)))
    rkb.add(KeyboardButton(text=_('📞 Biz bilan bog\'lanish', **kwargs)))
    rkb.add(KeyboardButton(text=_('🌐 Tilni almshtirish', **kwargs)))
    rkb.adjust(1,1,2,repeat=True)
    return rkb.as_markup(resize_keyboard=True)
