from aiogram import Router

from bot.handlers import main_router
from bot.order import order_router
from bot.inline_mode import inline_router
from bot.basket import basket_router
from bot.admins import administrator_router

BEGIN_router = Router()

BEGIN_router.include_routers(
    administrator_router,
    inline_router,
    basket_router,
    order_router,
    main_router,
)
