from enum import Enum
from typing import List

from sqlalchemy import BigInteger, VARCHAR, Float, SMALLINT, ForeignKey, String, INTEGER
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db import CreatedModel


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))
    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Product(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(20))
    image: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(VARCHAR(255))
    price: Mapped[float] = mapped_column(Float())
    discount_price: Mapped[float] = mapped_column(Float(), default=0.0)
    quantity: Mapped[int] = mapped_column(SMALLINT, default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship("Category", back_populates="products", cascade="all, delete")


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

    # def __repr__(self):
    #     return f"<Order(id={self.id}, user_id={self.user_id}, status={self.order_status}, date_time={self.date_time})>"


class Basket(CreatedModel):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(INTEGER, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped['Order'] = relationship('Order', back_populates='items')
    product: Mapped['Product'] = relationship('Product')

    # def __repr__(self):
    #     return f"<Basket(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})>"
