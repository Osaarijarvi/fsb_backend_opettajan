from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated

from db import get_db
from services.category_service import CategoryService

OpenSASession = Annotated[Session, Depends(get_db)]

def category_service_factory(_repository: OpenSASession) -> CategoryService:
    return CategoryService(_repository)