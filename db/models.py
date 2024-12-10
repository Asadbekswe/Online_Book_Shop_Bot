import uuid
from enum import Enum

from sqlalchemy import BigInteger, VARCHAR, Column, Integer
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.future import select
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import TimeBaseModel
from db.base import db


class User(TimeBaseModel):
    class Type(Enum):
        USER = "user"
        ADMIN = "admin"
        SUPER_ADMIN = "super_admin"

    first_name: Mapped[str] = mapped_column(VARCHAR(255))
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    type: Mapped[Type] = mapped_column(SQLEnum(Type), default=Type.USER)
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')
    baskets: Mapped['Basket'] = relationship('Basket', back_populates='user')


class Category(TimeBaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')

    def __repr__(self):
        return self.name


class Product(TimeBaseModel):
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    image: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float())
    discount_price: Mapped[float] = mapped_column(Float(), default=0.0)
    quantity: Mapped[int] = mapped_column(BigInteger, default=0)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product(uuid={self.uuid}, title={self.title})>"

    @classmethod
    async def get_products_by_category_id(cls, category_id):
        query = select(cls).where(cls.category_id == category_id)
        return (await db.execute(query)).scalars()


class Order(TimeBaseModel):
    class Status(Enum):
        DELIVERING = "☑️ Yetqazilmoqda"
        DELIVERED = "✅ Yetqazilgan"
        PENDING = "🕐 Kutish holatida"
        RETURNED = "⬅️ Qaytarilgan"
        CANCELLED = "❌ Bekor qilingan"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    order_status: Mapped[str] = mapped_column(
        String(50), default=Status.PENDING
    )
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    user: Mapped["User"] = relationship('User', back_populates='orders')
    items: Mapped[list['Basket']] = relationship('Basket', back_populates='order', cascade="all, delete")


class Basket(TimeBaseModel):
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('orders.id'), nullable=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('products.id'), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    order: Mapped['Order'] = relationship('Order', back_populates='items')
    product: Mapped['Product'] = relationship('Product')

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='baskets')
