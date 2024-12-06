# from enum import Enum
# from typing import List
#
# from sqlalchemy import VARCHAR, Float, SMALLINT, ForeignKey, BigInteger, Enum as SQLEnum
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from db.base import CreatedModel
# from db.models  import User
#
#
# class Category(CreatedModel):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(VARCHAR(20))
#     products: Mapped[List["Product"]] = relationship(back_populates="category")
#
#
# class Product(CreatedModel):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     price: Mapped[str] = mapped_column(Float())
#     name: Mapped[str] = mapped_column(VARCHAR(20))
#     quantity: Mapped[int] = mapped_column(SMALLINT, default=0)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped[List["User"]] = relationship(back_populates="products")
#     category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
#     category: Mapped[List["Category"]] = relationship(back_populates="products", cascade="all, delete")
#
#
# class Orders(CreatedModel):
#     class Status(Enum):
#         PENDING = "Kutish xolatida"
#         CONFIRMED = "Tasdiqlangan"
#         CANCELED = "Bekor qilingan"
#
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["User"] = relationship(back_populates="orders")
#     total_amount: Mapped[float] = mapped_column(Float, nullable=False)
#     status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.PENDING)
#     products: Mapped[List["Baskets"]] = relationship(
#         back_populates="order", cascade="all, delete"
#     )
#
#
# class Baskets(CreatedModel):
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
#     order: Mapped["Orders"] = relationship(back_populates="products")
#     product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
#     product: Mapped["Product"] = relationship()
#     quantity: Mapped[int] = mapped_column(SMALLINT, default=1)
#     price: Mapped[float] = mapped_column(Float, nullable=False)
