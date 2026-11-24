
from argon2 import PasswordHasher
from sqlalchemy.orm import Session

import models
from custom_exceptions.conflict_exception import ConflictException
from services.abc_user_service import ABCUserService


class UserService(ABCUserService):

    def __init__(self, _repository: Session):
        self._repository = _repository
        self.ph = PasswordHasher()

    def get_user_by_username(self, username: str) -> models.User | None:
        return self._repository.query(models.User).filter_by(username=username).first()

    def register(self, username: str, password: str) -> models.User:
        if self.get_user_by_username(username) is not None:
            raise ConflictException('username is already taken')

        # argon2.hash palauttaa merkkijonon, johon on pakattu sekä
        # algoritmin tunniste, parametrit, salt että itse hash.
        # Erillistä salt-saraketta ei siis tarvita.
        hashed_password = self.ph.hash(password)

        user = models.User(
            username=username,
            hashed_password=hashed_password,
            role='borrower',
        )

        self._repository.add(user)
        self._repository.commit()

        return user