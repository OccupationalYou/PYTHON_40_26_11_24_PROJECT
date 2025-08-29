from sqlalchemy import Column, Integer, Table, ForeignKey

from base import Base


user_products = Table(
    "user_product",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
)
