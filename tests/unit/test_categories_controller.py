
import unittest

from fastapi.testclient import TestClient

import models
from custom_exceptions.not_found_exception import NotFoundException
from factories.services import category_service_factory
from main import app
from tests.fakes import FakeCategoryService


class CategoriesControllerTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        # Siivotaan korvaukset, etteivät ne vuoda seuraaviin testeihin
        app.dependency_overrides.clear()


    def test_create_returns_201(self):
        app.dependency_overrides[category_service_factory] = lambda: FakeCategoryService()

        response = self.client.post('/api/categories/', json={'name': 'Kannettavat'})

        self.assertEqual(201, response.status_code)
        self.assertEqual('Kannettavat', response.json()['name'])

    def test_create_with_too_short_name_returns_422(self):
        app.dependency_overrides[category_service_factory] = lambda: FakeCategoryService()

        response = self.client.post('/api/categories/', json={'name': 'K'})

        self.assertEqual(422, response.status_code)


if __name__ == '__main__':
    unittest.main()