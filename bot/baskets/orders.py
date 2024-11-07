import asyncio
import datetime

from aiogram import F, Router, Bot
from aiogram.enums import ContentType, ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton, Message, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.baskets import to_category, basket_msg
from bot.config import db, ADMIN_LIST
from bot.keyboards import main_buttons

order_router = Router()


class BasketState(StatesGroup):
    phone_number = State()


def order_message(user_id, order_num):
    user_order = db['orders'][str(user_id)][str(order_num)]
    msg = _(
        '🔢 Buyurtma raqami: <b>{name}</b>\n📆 Buyurtma qilingan sana: <b>{date_time}</b>\n🟣 Buyurtma holati: <b>{order_status}</b>\n').format(
        name=order_num, date_time=user_order["date_time"], order_status=user_order["order_status"])

    all_sum = 0
    for i, v in enumerate(user_order['products'].values()):
        summa = int(v['quantity']) * int(v['price'])
        msg += f'\n{i + 1}. 📕 Kitob nomi: {v["product_name"]} \n{v["quantity"]} x {v["price"]} = {str(summa)} so\'m\n'
        all_sum += summa

    msg += f'\n💸 Umumiy narxi: {all_sum} so\'m'
    return msg


def clear_users_basket(user_id):
    basket_ = db['baskets']
    basket_.pop(str(user_id))
    db['baskets'] = basket_


@order_router.callback_query(F.data.startswith('clear'))
async def clear(callback: CallbackQuery):
    clear_users_basket(callback.from_user.id)
    await to_category(callback)


import asyncio


@order_router.callback_query(F.data.endswith('confirm'))
async def confirm(callback: CallbackQuery, state: FSMContext):
    rkb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=_('📞 Telefon raqam'), request_contact=True)]], resize_keyboard=True)

    await callback.message.delete()
    await callback.message.answer(
        _('Telefon raqamingizni qoldiring (📞 Telefon raqam tugmasini bosing): 👇🏻'),
        reply_markup=rkb
    )

    await state.set_state(BasketState.phone_number)
    msg = await callback.answer(
        _('📞 Raqamingiz qabul qilindi. Tashakkur!'),
        reply_markup=main_buttons()
    )
    await asyncio.sleep(3)
    await callback.msg.delete()


@order_router.message(F.content_type == ContentType.CONTACT, BasketState.phone_number)
async def phone_number(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer(_("Telefon raqamingizni olishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring."))
        return

    msg = f"{basket_msg(message.from_user.id)}\nTelefon raqamingiz: {message.contact.phone_number}\n\n<i>Buyurtma berasizmi?</i>"
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text=_("❌ Yo'q"), callback_data='canceled_order'),
        InlineKeyboardButton(text=_('✅ Ha'), callback_data=f'confirm_order_{message.contact.phone_number}')
    )

    await message.answer(msg, reply_markup=ikb.as_markup())
    await state.clear()


@order_router.callback_query(F.data.endswith('canceled_order'))
async def canceled_order(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(_('❌ Bekor qilindi'))
    await callback.message.answer(_('Asosiy menyu'), reply_markup=main_buttons())


@order_router.callback_query(F.data.startswith('confirm_order'))
async def confirm_order(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()

    orders = db.get('orders', {})
    orders['order_num'] = orders.get('order_num', 0) + 1

    user_id = str(callback.from_user.id)
    if user_id not in orders:
        orders[user_id] = {}

    orders[user_id][str(orders['order_num'])] = {
        'date_time': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        'order_status': '🔄 kutish holatida',
        'products': db.get('baskets', {}).get(user_id, {}),
        'phone_number': callback.data[13:]
    }

    db['orders'] = orders
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=_("❌ Yo'q"),
                callback_data=f'from_admin_canceled_order-{user_id}-{orders["order_num"]}'
            ),
            InlineKeyboardButton(
                text=_('✅ Ha'),
                callback_data=f'from_admin_order_accept-{user_id}-{orders["order_num"]}'
            )
        ]
    ])

    user_full_name = callback.from_user.full_name or _("Foydalanuvchi")

    if not ADMIN_LIST:
        await callback.message.answer(_("Admin list is empty; unable to notify admin."))
        return

    try:
        await bot.send_message(
            ADMIN_LIST[0],
            order_message(callback.from_user.id, orders["order_num"]) +
            f"\n\nKlient: +{callback.data[12:].replace('r_', '')} <a href='tg://user?id={callback.from_user.id}'>{user_full_name}</a>\nBuyurtmani qabul qilasizmi?",
            parse_mode=ParseMode.HTML,
            reply_markup=ikb
        )
    except TelegramBadRequest as e:
        print(f"Error sending message: {e}")

    await callback.message.answer(
        _('✅ Hurmatli mijoz! Buyurtmangiz uchun tashakkur.\nBuyurtma raqami: {orders_num}').format(
            orders_num=orders["order_num"]
        ),
        reply_markup=main_buttons()
    )

    clear_users_basket(callback.from_user.id)


@order_router.callback_query(F.data.startswith('from_admin'))
async def order_accept_canceled(callback: CallbackQuery, bot: Bot):
    user_order = callback.data.split('-')[1:]
    orders = db['orders']
    users_orders = orders[user_order[0]]
    if callback.data.startswith('from_admin_order_accept'):
        users_orders[user_order[1]]['order_status'] = '✅ Zakaz qabul qilingan'
        await bot.send_message(user_order[0],
                               _('<i>🎉 Sizning {order_num} raqamli buyurtmangizni admin qabul qildi.</i>').format(
                                   order_num=user_order[1]))
        await callback.message.edit_reply_markup()
    else:
        await callback.message.delete()
        users_orders.pop(user_order[1])
    db['orders'] = orders


@order_router.message(F.text == __('📃 Mening buyurtmalarim'))
async def my_orders(message: Message):
    user_id = str(message.from_user.id)
    if 'orders' not in db:
        db['orders'] = {}
    if user_id not in db['orders'] or not db['orders'][user_id]:
        await message.answer(_('🤷‍♂️ Sizda hali buyurtmalar mavjud emas. Yoki bekor qilingan'))
    else:
        for order in db['orders'][user_id].keys():
            ikb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=_('❌ bekor qilish'), callback_data='from_user_canceled_order' + order)]
            ])

            await message.answer(order_message(user_id, order), reply_markup=ikb)


@order_router.callback_query(F.data.startswith('from_user_canceled_order'))
async def canceled_order(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    orders = db['orders']
    order_num = callback.data.split('from_user_canceled_order')[-1]
    orders[str(callback.from_user.id)].pop(order_num)
    db['orders'] = orders
    await callback.message.answer(f'{order_num} raqamli buyurtmangiz bekor qilindi')
    await bot.send_message(ADMIN_LIST[0],
                           f'{order_num} raqamli buyurtma bekor qilindi\n\nZakaz egasi {callback.from_user.mention_markdown(callback.from_user.full_name)}',
                           parse_mode=ParseMode.MARKDOWN_V2)
