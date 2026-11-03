

from sqlalchemy.orm import Session

import models
from custom_exceptions.not_found_exception import NotFoundException
from dtos.categories import CreateCategoryReq
from services.abc_category_service import ABCCategoryService
from custom_exceptions.business_rule_exception import BusinessRuleException


class CategoryService(ABCCategoryService):

    def __init__(self, _repository: Session):
        self._repository = _repository

    # Hae kaikki luokat
    def get_all(self) -> list[models.Category]:
        return self._repository.query(models.Category).all()

    # Löydä luokka ID:n avulla
    def get_by_id(self, _id: int) -> models.Category:
        category = self._repository.query(models.Category).filter_by(id=_id).first()

        if category is None:
            raise NotFoundException(f'category {_id} not found')

        return category

    # Lisää luokka
    def create(self, req: CreateCategoryReq) -> models.Category:
        category = models.Category(name=req.name)

        self._repository.add(category)
        self._repository.commit()

        return category

    # Päivitä luokka
    def update(self, _id: int, req: CreateCategoryReq) -> models.Category:
        category = self.get_by_id(_id)

        category.name = req.name
        self._repository.commit()

        return category

    # Poista luokka
    def delete(self, _id: int) -> None:
        category = self.get_by_id(_id)

        # Speksi: kategoriaa ei saa poistaa, jos siinä on nimikkeitä
        if category.items:
            raise BusinessRuleException(f'category {_id} still has items')

        self._repository.delete(category)
        self._repository.commit()