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


