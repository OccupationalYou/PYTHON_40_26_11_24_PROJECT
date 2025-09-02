
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from .associations import user_products
from flask_login import UserMixin

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    products: Mapped[list["Product"]] = relationship(

        "Product",
        secondary=user_products,
        back_populates="users"
    )