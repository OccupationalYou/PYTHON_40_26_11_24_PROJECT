
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from .associations import user_products

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    description: Mapped[str] = mapped_column()

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_products,
        back_populates="products"
    )
