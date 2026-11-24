#from sqlalchemy.sql.annotation import Annotated

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from services.category_service import CategoryService
from services.user_service import UserService

OpenSASession = Annotated[Session, Depends(get_db)]

def category_service_factory(_repository: OpenSASession) -> CategoryService:
    return CategoryService(_repository)


def user_service_factory(_repository: OpenSASession) -> UserService:
    return UserService(_repository)