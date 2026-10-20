from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from services.category_service import CategoryService


def category_service_factory(repository: Session = Depends(get_db)):
    return CategoryService(repository)