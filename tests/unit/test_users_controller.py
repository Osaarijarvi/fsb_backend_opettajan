
import unittest

from fastapi.testclient import TestClient

import models
from custom_exceptions.conflict_exception import ConflictException
from factories.services import user_service_factory
from main import app
from tests.fakes import FakeUserService


def make_user():
    return models.User(id=1, username='matti', role='borrower',
                       hashed_password='$argon2id$erittain-salainen')


class UsersControllerTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_register_returns_201_and_user(self):
        app.dependency_overrides[user_service_factory] = \
            lambda: FakeUserService(user=make_user())

        response = self.client.post('/api/users/register',
                                    json={'username': 'matti', 'password': 'salasana123'})

        self.assertEqual(201, response.status_code)
        self.assertEqual('matti', response.json()['username'])
        self.assertEqual('borrower', response.json()['role'])

    def test_register_does_not_leak_password_hash(self):
        app.dependency_overrides[user_service_factory] = \
            lambda: FakeUserService(user=make_user())

        response = self.client.post('/api/users/register',
                                    json={'username': 'matti', 'password': 'salasana123'})

        body = response.json()

        self.assertNotIn('hashed_password', body)
        self.assertNotIn('password', body)
        # varmistetaan vielä koko vastauksen tekstistä
        self.assertNotIn('argon2', response.text)

    def test_register_with_taken_username_returns_409(self):
        app.dependency_overrides[user_service_factory] = \
            lambda: FakeUserService(raises=ConflictException('username is already taken'))

        response = self.client.post('/api/users/register',
                                    json={'username': 'matti', 'password': 'salasana123'})

        self.assertEqual(409, response.status_code)

    def test_register_with_too_short_password_returns_422(self):
        app.dependency_overrides[user_service_factory] = \
            lambda: FakeUserService(user=make_user())

        response = self.client.post('/api/users/register',
                                    json={'username': 'matti', 'password': 'lyhyt'})

        self.assertEqual(422, response.status_code)


if __name__ == '__main__':
    unittest.main()