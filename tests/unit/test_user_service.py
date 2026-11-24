
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from custom_exceptions.conflict_exception import ConflictException
from db import Base
from services.user_service import UserService


class UserServiceTests(unittest.TestCase):

    def setUp(self):
        # sqlite:///:memory: luo tietokannan muistiin.
        # setUp ajetaan ennen jokaista testiä, joten
        # jokainen testi saa oman tyhjän kantansa.
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        self.service = UserService(self.session)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_register_creates_user_with_role_borrower(self):
        # Act
        user = self.service.register('matti', 'salasana123')

        # Assert
        self.assertIsNotNone(user.id)
        self.assertEqual('matti', user.username)
        self.assertEqual('borrower', user.role)

    def test_register_hashes_the_password(self):
        user = self.service.register('matti', 'salasana123')

        # Salasana ei saa olla tallessa selkokielisenä
        self.assertNotEqual('salasana123', user.hashed_password)
        # argon2-hash alkaa aina algoritmin tunnisteella
        self.assertTrue(user.hashed_password.startswith('$argon2'))

    def test_register_same_username_twice_raises_conflict(self):
        self.service.register('matti', 'salasana123')

        with self.assertRaises(ConflictException) as ctx:
            self.service.register('matti', 'toinen-salasana')

        self.assertIn('already taken', str(ctx.exception))

    def test_get_user_by_username_returns_none_when_not_found(self):
        self.assertIsNone(self.service.get_user_by_username('ei-ole'))


if __name__ == '__main__':
    unittest.main()