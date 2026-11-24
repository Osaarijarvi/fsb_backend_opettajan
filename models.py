
from sqlalchemy import Integer, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # unique=True: kahta samannimistä kategoriaa ei ole järkeä olla
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    role: Mapped[str] = mapped_column(Text, nullable=False, server_default=text("'borrower'"))
    # argon2 tallentaa saltin osaksi hash-merkkijonoa,
    # joten erillistä salt-saraketta ei tarvita
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)