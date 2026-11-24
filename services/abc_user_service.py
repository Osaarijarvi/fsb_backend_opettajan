
import abc

import models


class ABCUserService(abc.ABC):
    @abc.abstractmethod
    def register(self, username: str, password: str) -> models.User | None:
        raise NotImplementedError()  # pragma: no cover

    @abc.abstractmethod
    def get_user_by_username(self, username: str) -> models.User | None:
        raise NotImplementedError()  # pragma: no cover