from enum import Enum
from typing import List

from sqlalchemy import ForeignKey, BigInteger, VARCHAR, Float, SMALLINT, Enum as SQLEnum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.base import CreatedModel


class User(CreatedModel):
    class Type(Enum):
        USER = "user"
        ADMIN = "admin"
        SUPER_ADMIN = "super_admin"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255))
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    type: Mapped[Type] = mapped_column(SQLEnum(Type), default=Type.USER)
    products: Mapped[List["Product"]] = relationship(back_populates="user", cascade="all, delete")


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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[List["User"]] = relationship(back_populates="products")
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    category: Mapped[List["Category"]] = relationship(back_populates="products", cascade="all, delete")
