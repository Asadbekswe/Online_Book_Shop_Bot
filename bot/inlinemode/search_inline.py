from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent, Message, FSInputFile

from bot.keyboards import make_plus_minus
from db import Product

inline_router = Router()


@inline_router.message(
    lambda msg: msg.text is not None and str(msg.text[-36:]) == "35f22a34-25b7-4f75-b463-2390ffb24d20")
async def answer_inline_query(message: Message):
    msg = message.text[-36:]
    product = await Product.get(id_=1)
    ikb = make_plus_minus(1, msg)
    await message.delete()
    await message.answer_photo(photo=FSInputFile(product.image), caption=product.description,
                               reply_markup=ikb.as_markup())


@inline_router.inline_query()
async def user_inline_handler(inline_query: InlineQuery):
    # if inline_query.query == "":
    #     inline_mode_books_list = []
    #     for count, (product_key, product_val) in enumerate(db['products'].items()):
    #         inline_mode_books_list.append(InlineQueryResultArticle(
    #             id=product_key,
    #             title=product_val['name'],
    #             input_message_content=InputTextMessageContent(
    #                 message_text=f"<i>{product_val['text'][2:]}</i>Buyurtma qilish uchun  : @worldbooks_storebot\n\nbook_id: {product_key}"
    #             ),
    #             thumbnail_url=product_val['thumbnail_url'],
    #             description=f"World Books Store\n💵 Narxi: {product_val['price']} so'm",
    #         ))
    #         if count == 50:
    #             break
    #     await inline_query.answer(inline_mode_books_list)
    # else:
    #     products = {key: val for key, val in db['products'].items() if inline_query.query.lower() in val['name'].lower()}
    #     inline_mode_books_list = []
    #     for count, (product_key, product_val) in enumerate(products.items()):
    #         inline_mode_books_list.append(InlineQueryResultArticle(
    #             id=product_key,
    #             title=product_val['name'],
    #             input_message_content=InputTextMessageContent(
    #                 message_text=f"<i>{product_val['text'][2:]}</i>Buyurtma qilish uchun  : @worldbooks_storebot\n\nbook_id: {product_key}"
    #             ),
    #             thumbnail_url=product_val['thumbnail_url'],
    #             description=f"World Books Store\n💵 Narxi: {product_val['price']} so'm",
    #         ))
    #         if count == 50:
    #             break
    #     await inline_query.answer(inline_mode_books_list)

    products = await Product.get_all()
    query = inline_query.query.lower()
    filtered_products = [
        product for product in products
        if query in product.title.lower()
    ]

    inline_mode_books_list = []
    for product in filtered_products:
        # thumbnail_url = f"{BASE_URL}/{MEDIA_DIRECTORY}/{product.image}"
        inline_mode_books_list.append(InlineQueryResultArticle(
            id=str(product.uuid),
            title=product.title,
            input_message_content=InputTextMessageContent(
                message_text=(
                    f"<i>{product.description}</i>\n\n"
                    f"Buyurtma qilish uchun: @worldbooks_storebot\n\n"
                    f"book_id: {product.uuid}"
                )
            ),
            thumbnail_url="https://www.google.com/imgres?q=image&imgurl=https%3A%2F%2Fdfstudio-d420.kxcdn.com%2Fwordpress%2Fwp-content%2Fuploads%2F2019%2F06%2Fdigital_camera_photo-1080x675.jpg&imgrefurl=https%3A%2F%2Fwww.dfstudio.com%2Fdigital-image-size-and-resolution-what-do-you-need-to-know%2F&docid=KEFtss0dYCDpzM&tbnid=0kl2WrGN8BrkhM&vet=12ahUKEwjW3IiD85WKAxWWExAIHZidKioQM3oECF0QAA..i&w=1080&h=675&hcb=2&ved=2ahUKEwjW3IiD85WKAxWWExAIHZidKioQM3oECF0QAA",
            description=f"World Books Store\n💵 Narxi: {product.price} so'm",
        ))

    await inline_query.answer(inline_mode_books_list)
