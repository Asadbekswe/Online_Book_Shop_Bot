from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.configs import db
from bot.keyboards import show_category, make_plus_minus

basket_router = Router()


def basket_msg(user_id):
    basket_of_user = db['baskets'][str(user_id)]
    msg = f'🛒 Savat \n\n'
    all_sum = 0
    for key, val in enumerate(basket_of_user.values()):
        summa = val['quantity'] * float(val['price'])
        msg += f'{key + 1}. {val["product_name"]} \n{val["quantity"]} x {val["price"]} = {str(summa)} so\'m\n\n'
        all_sum += summa
    msg += _("Jami: {all_sum} so\'m").format(all_sum=all_sum)
    return msg


@basket_router.callback_query(F.data.startswith('categoryga'))
async def to_category(callback: CallbackQuery):
    quantity = 1
    await callback.message.delete()
    await callback.message.answer(_('Categoriyalardan birini tanlang 👇🏻'),
                                  reply_markup=show_category(callback.from_user.id))


@basket_router.callback_query(F.data.startswith('savatga'))
async def to_basket(callback: CallbackQuery):
    basket_ = db['baskets']
    user = basket_.get(str(callback.from_user.id))
    product_id = callback.data[7:43]
    product = db['products'][product_id]
    if user:
        if user.get(product_id):
            user[product_id]['quantity'] += int(callback.data[43:])
        else:
            user[product_id] = {
                'product_name': product['name'],
                'quantity': callback.data[43:],
                'price': product['price']
            }
    else:
        basket_[str(callback.from_user.id)] = {
            product_id: {
                'product_name': product['name'],
                'quantity': int(callback.data[43:]),
                'price': product['price']
            }
        }
    db['baskets'] = basket_
    await to_category(callback)


quantity = 1


@basket_router.callback_query(F.data.startswith("change"))
async def change_plus(callback: CallbackQuery):
    global quantity
    if callback.data.startswith("change+"):
        quantity += 1
    elif quantity < 2:
        await callback.answer(_('Eng kamida 1 ta kitob buyurtma qilishingiz mumkin! 😊'), show_alert=True)
        return
    else:
        quantity -= 1
    ikb = make_plus_minus(quantity, callback.data[7:])
    await callback.message.edit_reply_markup(str(callback.message.message_id), reply_markup=ikb.as_markup())


@basket_router.callback_query(F.data.startswith('savat'))
async def basket(callback: CallbackQuery):
    msg = basket_msg(callback.from_user.id)
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text=_('❌ Savatni tozalash'), callback_data='clear'))
    ikb.row(InlineKeyboardButton(text=_('✅ Buyurtmani tasdiqlash'), callback_data='confirm'))
    ikb.row(InlineKeyboardButton(text=_('◀️ orqaga'), callback_data='categoryga'))
    await callback.message.edit_text(msg, reply_markup=ikb.as_markup())
