from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped


class AdminModel(BaseModel):



class CategoryModel(BaseModel):
    name: Mapped[str] = mapped_column(String(255))


class ProductModel(BaseModel):
    title: Mapped[str] = mapped_column(String(255), primary_key=True)
    description: Mapped[String] = mapped_column(String(255))
    price: Mapped[int] = mapped_column(String(255))


