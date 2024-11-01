from uuid import uuid4

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import db
from bot.filters.is_admin import ChatTypeFilter, IsAdmin
from bot.keyboards import show_category, admin_buttons
from bot.utils.uploader import make_url

administrator_router = Router()
administrator_router.message.filter(ChatTypeFilter([ChatType.PRIVATE]), IsAdmin())


@administrator_router.message(CommandStart())
async def start_for_admin(message: Message):
    await message.answer('Tanlovingiz ❕', reply_markup=admin_buttons())


class FormAdministrator(StatesGroup):
    product_name = State()
    product_price = State()
    product_photo = State()
    product_description = State()
    product_category = State()
    category = State()
    see_category = State()
    product_delete = State()
    category_delete = State()


storage = {}


@administrator_router.message(F.text == 'Product+')
async def add_product(message: Message, state: FSMContext):
    if not db['categories']:
        await message.answer("Product qo'shishdan avval Category kiritish zarur ⁉️")
        return
    await state.set_state(FormAdministrator.product_name)
    await message.answer('Product nomini kiriting 👇🏻', reply_markup=ReplyKeyboardRemove())


@administrator_router.message(FormAdministrator.product_name)
async def add_product(message: Message, state: FSMContext):
    storage['name'] = message.text
    await state.set_state(FormAdministrator.product_description)
    await message.answer('Product description kiriting 👇🏻')


@administrator_router.message(FormAdministrator.product_description)
async def add_product(message: Message, state: FSMContext):
    storage['text'] = message.text
    await state.set_state(FormAdministrator.product_photo)
    await message.answer("Product rasmini jo'nating 👇🏻 ")


@administrator_router.message(FormAdministrator.product_photo)
async def add_product(message: Message, state: FSMContext):
    url = await make_url(
        ((await message.bot.download((await message.bot.get_file(message.photo[-1].file_id)).file_id)).read()))
    storage['image'] = message.photo[0].file_id
    storage['thumbnail_url'] = url
    await state.set_state(FormAdministrator.product_price)
    await message.answer('Product narxini kiriting 👇🏻 ')


@administrator_router.message(FormAdministrator.product_price)
async def add_product(message: Message, state: FSMContext):
    storage['price'] = message.text
    await state.set_state(FormAdministrator.product_category)
    await message.answer('Categoryni tanlang 👇🏻', reply_markup=show_category(message.from_user.id))


@administrator_router.callback_query(FormAdministrator.product_category)
async def add_product(callback: CallbackQuery, state: FSMContext):
    if callback.data not in db['categories']:
        await callback.answer('Category tanlashda xatolik Mavjud ‼️')
        return
    storage['category_id'] = callback.data
    product = db['products']
    product[str(uuid4())] = storage
    db['products'] = product
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Saqlandi ✅', reply_markup=admin_buttons())


@administrator_router.message(F.text == 'Category+')
async def add_category(message: Message, state: FSMContext):
    await state.set_state(FormAdministrator.category)
    await message.answer('Category nomini kiriting 👇🏻', reply_markup=ReplyKeyboardRemove())


@administrator_router.message(FormAdministrator.category)
async def add_category(message: Message, state: FSMContext) -> None:
    category = db['categories']
    category[str(uuid4())] = message.text
    db['categories'] = category
    await state.clear()
    await message.answer("Catgory Bazaga Saqlandi ✅", reply_markup=admin_buttons())


@administrator_router.message(F.text == 'delete product')
async def category_delete(message: Message, state: FSMContext) -> None:
    await message.answer('Tanlang', reply_markup=ReplyKeyboardRemove())
    await message.reply('👇🏻', reply_markup=show_category(message.from_user.id))
    await state.set_state(FormAdministrator.see_category)


@administrator_router.callback_query(FormAdministrator.product_delete)
async def product_delete(callback: CallbackQuery, state: FSMContext):
    products = db['products']
    products.pop(callback.data)
    db['products'] = products
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('Product deleted ✅', reply_markup=admin_buttons())


@administrator_router.message(F.text == 'Delete category')
async def category_delete(message: Message, state: FSMContext) -> None:
    await message.answer('Tanlang', reply_markup=ReplyKeyboardRemove())
    await message.reply('👇🏻', reply_markup=show_category(message.from_user.id))
    await state.set_state(FormAdministrator.category_delete)


@administrator_router.callback_query(FormAdministrator.category_delete)
async def category_delete(callback: CallbackQuery, state: FSMContext) -> None:
    new_products = {}
    for key, val in db['products'].items():
        if val['category_id'] != callback.data:
            new_products[key] = val
    db['products'] = new_products
    category = db['categories']
    category.pop(callback.data)
    db['categories'] = category
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text="Categoryga tegishli bo'lgan product va category o'chirildi ✅",
                                  reply_markup=admin_buttons())


@administrator_router.callback_query(FormAdministrator.see_category)
async def show_product(callback: CallbackQuery, state: FSMContext):
    ikb = InlineKeyboardBuilder()
    for key, val in db['products'].items():
        if val['category_id'] == callback.data:
            ikb.add(InlineKeyboardButton(text=val['name'], callback_data=key))
    ikb.adjust(2, repeat=True)
    await callback.message.edit_text(db['categories'][callback.data], reply_markup=ikb.as_markup())
    await state.set_state(FormAdministrator.product_delete)
