from typing import List

from sqlalchemy import ForeignKey, BigInteger, VARCHAR, Float, SMALLINT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.base import CreatedModel


class User(CreatedModel):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255))
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    products: Mapped[List["Product"]] = relationship(back_populates="user", cascade="all, delete")


class Category(CreatedModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(20))
    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Product(CreatedModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[str] = mapped_column(Float())
    name: Mapped[str] = mapped_column(VARCHAR(20))
    quantity: Mapped[int] = mapped_column(SMALLINT, default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[List["User"]] = relationship(back_populates="products")
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    category: Mapped[List["Category"]] = relationship(back_populates="products", cascade="all, delete")
