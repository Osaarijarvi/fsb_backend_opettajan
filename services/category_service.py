

from sqlalchemy.orm import Session

import models
from custom_exceptions.not_found_exception import NotFoundException
from dtos.categories import CreateCategoryReq
from services.abc_category_service import ABCCategoryService


class CategoryService(ABCCategoryService):

    def __init__(self, _repository: Session):
        self._repository = _repository

    def get_all(self) -> list[models.Category]:
        return self._repository.query(models.Category).all()

    def get_by_id(self, _id: int) -> models.Category:
        category = self._repository.query(models.Category).filter_by(id=_id).first()

        if category is None:
            raise NotFoundException(f'category {_id} not found')

        return category

    def create(self, req: CreateCategoryReq) -> models.Category:
        category = models.Category(name=req.name)

        self._repository.add(category)
        self._repository.commit()

        return category

    def update(self, _id: int, req: CreateCategoryReq) -> models.Category:
        category = self.get_by_id(_id)

        category.name = req.name
        self._repository.commit()

        return category

    def delete(self, _id: int) -> None:
        category = self.get_by_id(_id)

        self._repository.delete(category)
        self._repository.commit()