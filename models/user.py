
from sqlalchemy.orm import Mapped, mapped_column, relationship
from base import Base
from .associations import user_products
from flask_login import UserMixin

class User(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    products: Mapped[list["Product"]] = relationship(

        "Product",
        secondary=user_products,
        back_populates="users"
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
