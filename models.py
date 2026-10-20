
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # unique=True: kahta samannimistä kategoriaa ei ole järkeä olla
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)