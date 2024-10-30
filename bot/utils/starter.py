from aiogram import Router

from bot.admins import administrator_router
from bot.baskets import order_router
from bot.baskets.basket import basket_router
from bot.handlers import main_router
from bot.inline_mode import inline_router

BEGIN_router = Router()

BEGIN_router.include_routers(
    administrator_router,
    inline_router,
    basket_router,
    order_router,
    main_router,
)
