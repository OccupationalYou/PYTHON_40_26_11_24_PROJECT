from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String)

    # Исправленный внешний ключ, ссылающийся на users.id
    user_id = Column(Integer, ForeignKey('users.id'))

    # Установка обратной связи с моделью User
    user = relationship('User', back_populates='products')

    def __init__(self, name, description, price, image_url, user_id):
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.user_id = user_id

    def __repr__(self):
        return f"<Product({self.name})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url,
            "user_id": self.user_id,
        }
