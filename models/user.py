from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    products = relationship('Product', back_populates='user')

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Flask-Login требует этот атрибут
        self.is_active = True

    def __repr__(self):
        return f"<User({self.username})>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }

    def get_id(self):
        return str(self.id)
