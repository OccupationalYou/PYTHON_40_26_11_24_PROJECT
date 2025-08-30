<<<<<<< HEAD
<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, Table, ForeignKey

from base import Base


user_products = Table(
    "user_product",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
=======
from sqlalchemy import Column, Integer, Table, ForeignKey

from base import Base


user_products = Table(
    "user_product",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
>>>>>>> Stashed changes
)
=======
from sqlalchemy import Table, Column, Integer, ForeignKey
from base import Base

user_products = Table(
    "user_products",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)
>>>>>>> e1c03cece7392e360da7ab2d96d83aa0e9cccd3e
