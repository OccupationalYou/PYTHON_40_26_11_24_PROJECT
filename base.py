import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


basedir = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(basedir, "shop.db")


engine = create_engine(f"sqlite:///{db_path}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    ...


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)
