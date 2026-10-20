
from typing import List

import models
from dtos.categories import CreateCategoryReq
from services.abc_category_service import ABCCategoryService


class FakeCategoryService(ABCCategoryService):
    # Konstruktorin kautta säädetään, miten fake käyttäytyy.
    # Näin sama luokka kelpaa moneen eri testiin.
    def __init__(self, categories: List[models.Category] = None, raises: Exception = None):
        self._categories = categories or []
        self._raises = raises

    def get_all(self) -> List[models.Category]:
        return self._categories

    def get_by_id(self, _id: int) -> models.Category:
        if self._raises:
            raise self._raises
        return self._categories[0]

    def create(self, req: CreateCategoryReq) -> models.Category:
        return models.Category(id=1, name=req.name)

    def update(self, _id: int, req: CreateCategoryReq) -> models.Category:
        if self._raises:
            raise self._raises
        return models.Category(id=_id, name=req.name)

    def delete(self, _id: int) -> None:
        if self._raises:
            raise self._raises