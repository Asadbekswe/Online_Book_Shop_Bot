from enum import Enum

from sqlalchemy import BigInteger, VARCHAR, Float, SMALLINT, ForeignKey, String, INTEGER, Text
from sqlalchemy.future import select
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import db, CreatedModel


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')


class Product(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    image: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float())
    discount_price: Mapped[float] = mapped_column(Float(), default=0.0)
    quantity: Mapped[int] = mapped_column(SMALLINT, default=0)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', back_populates='products')

    @classmethod
    async def get_products_by_category_id(cls, category_id):
        query = select(cls).where(cls.category_id == category_id)
        return (await db.execute(query)).scalars()


class Order(CreatedModel):
    class Status(Enum):
        DELIVERING = "☑️ Yetqazilmoqda"
        DELIVERED = "✅ Yetqazilgan"
        PENDING = "🕐 Kutish holatida"
        RETURNED = "⬅️ Qaytarilgan"
        CANCELLED = "❌ Bekor qilingan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    order_status: Mapped[str] = mapped_column(
        String(50), default=Status.PENDING
    )
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    user: Mapped["User"] = relationship('User', back_populates='orders')
    items: Mapped[list['Basket']] = relationship('Basket', back_populates='order', cascade="all, delete")


class Basket(CreatedModel):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(INTEGER, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped['Order'] = relationship('Order', back_populates='items')
    product: Mapped['Product'] = relationship('Product')
