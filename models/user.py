from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import Integer, String
from base import Base
from models.associations import user_products
from models.product import Product

class User(Base):
    tablename = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product", secondary=user_products, back_populates="users"
    )
