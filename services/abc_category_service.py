
import abc

import models
from dtos.categories import CreateCategoryReq


class ABCCategoryService(abc.ABC):
    @abc.abstractmethod
    def get_all(self) -> list[models.Category]:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def get_by_id(self, _id: int) -> models.Category:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def create(self, req: CreateCategoryReq) -> models.Category:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def update(self, _id: int, req: CreateCategoryReq) -> models.Category:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def delete(self, _id: int) -> None:
        raise NotImplementedError()  # pragma: no cover