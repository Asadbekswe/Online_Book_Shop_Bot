from enum import Enum

from sqlalchemy import BigInteger, VARCHAR
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.base import CreatedModel
from db.models.shop import Order,Basket


class User(CreatedModel):
    class Type(Enum):
        USER = "user"
        ADMIN = "admin"
        SUPER_ADMIN = "super_admin"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(VARCHAR(255))
    last_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    phone_number: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    type: Mapped[Type] = mapped_column(SQLEnum(Type), default=Type.USER)
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')
    baskets: Mapped['Basket'] = relationship('Basket', back_populates='user')

