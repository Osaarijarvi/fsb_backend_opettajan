

import models
from dtos.categories import CreateCategoryReq
from services.abc_category_service import ABCCategoryService
from services.abc_user_service import ABCUserService


class FakeCategoryService(ABCCategoryService):
    # Konstruktorin kautta säädetään, miten fake käyttäytyy.
    # Näin sama luokka kelpaa moneen eri testiin.
    def __init__(self, categories: list[models.Category] | None = None, raises: Exception | None = None):
        self._categories = categories or []
        self._raises = raises

    def get_all(self) -> list[models.Category] :
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


class FakeUserService(ABCUserService):
    def __init__(self, user: models.User | None = None, raises: Exception | None  = None):
        self._user = user
        self._raises = raises

    def register(self, username: str, password: str) -> models.User:
        if self._raises:
            raise self._raises
        return self._user

    def get_user_by_username(self, username: str) -> models.User | None:
        return self._user

    def login(self, username: str, password: str) -> str:
        if self._raises:
            raise self._raises
        return 'fake-token'

    def get_user_by_access_token(self, access_token: str) -> models.User | None:
        return self._user