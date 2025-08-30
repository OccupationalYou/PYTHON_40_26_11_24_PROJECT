from sqlalchemy import Table, Column, Integer, ForeignKey
from base import Base

user_products = Table(
    "user_products",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_id", Integer, ForeignKey("products.id"))
)
