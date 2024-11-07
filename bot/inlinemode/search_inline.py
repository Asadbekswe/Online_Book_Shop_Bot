from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

from bot.config import db

inline_router = Router()


@inline_router.inline_query()
async def user_inline_handler(inline_query: InlineQuery):
    if inline_query.query == "":
        inline_mode_books_list = []
        for count, (product_key, product_val) in enumerate(db['products'].items()):
            inline_mode_books_list.append(InlineQueryResultArticle(
                id=product_key,
                title=product_val['name'],
                input_message_content=InputTextMessageContent(
                    message_text=f"<i>{product_val['text'][2:]}</i>Buyurtma qilish uchun  : @worldbooks_storebot\n\nbook_id: {product_key}"
                ),
                thumbnail_url=product_val['thumbnail_url'],
                description=f"World Books Store\n💵 Narxi: {product_val['price']} so'm",
            ))
            if count == 50:
                break
        await inline_query.answer(inline_mode_books_list)
    else:
        products = {k: v for k, v in db['products'].items() if inline_query.query.lower() in v['name'].lower()}
        inline_mode_books_list = []
        for count, (product_key, product_val) in enumerate(products.items()):
            inline_mode_books_list.append(InlineQueryResultArticle(
                id=product_key,
                title=product_val['name'],
                input_message_content=InputTextMessageContent(
                    message_text=f"<i>{product_val['text'][2:]}</i>Buyurtma qilish uchun  : @facror_book_bot\n\nbook_id: {product_key}"
                ),
                thumbnail_url=product_val['thumbnail_url'],
                description=f"Factor Books\n💵 Narxi: {product_val['price']} so'm",
            ))
            if count == 50:
                break
        await inline_query.answer(inline_mode_books_list)