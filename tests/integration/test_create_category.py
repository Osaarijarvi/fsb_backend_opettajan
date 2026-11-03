
from sqlalchemy import select

import models
from tests.integration.base import IntegrationTestCase

URL = "/api/categories/"


class TestCreateCategory(IntegrationTestCase):
    def get_saved_categories(self) -> list[models.Category]:
        # Haetaan testikannasta suoraan, ei luoteta API:n paluuarvoon
        return list(self.session.scalars(select(models.Category)))

    def test_returns_201_and_created_category(self):
        response = self.client.post(URL, json={"name": "Työkalut"})

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["name"], "Työkalut")
        self.assertIsInstance(body["id"], int)

    def test_saves_category_to_database(self):
        response = self.client.post(URL, json={"name": "Työkalut"})

        saved = self.get_saved_categories()
        self.assertEqual(len(saved), 1)
        # Vastauksen id:n pitää olla sama kuin kantaan tallentuneen rivin id
        self.assertEqual(saved[0].id, response.json()["id"])
        self.assertEqual(saved[0].name, "Työkalut")

    def test_two_categories_get_different_ids(self):
        first = self.client.post(URL, json={"name": "Työkalut"}).json()
        second = self.client.post(URL, json={"name": "Urheilu"}).json()

        self.assertNotEqual(first["id"], second["id"])
        self.assertEqual(len(self.get_saved_categories()), 2)

    def test_accepts_name_at_length_limits(self):
        # Nimen pituusrajat tulevat CreateCategoryReq-DTO:sta: min_length=2, max_length=50.
        # subTest ajaa saman tarkistuksen jokaiselle arvolle ja raportoi epäonnistumiset erikseen
        for name in ["ab", "a" * 50]:
            with self.subTest(name=name):
                response = self.client.post(URL, json={"name": name})

                self.assertEqual(response.status_code, 201)
                self.assertEqual(response.json()["name"], name)

    def test_invalid_name_returns_422_and_saves_nothing(self):
        cases = {
            "missing-name": {},
            "null-name": {"name": None},
            "empty-name": {"name": ""},
            "too-short": {"name": "a"},
            "too-long": {"name": "a" * 51},
        }
        for case, payload in cases.items():
            with self.subTest(case=case):
                response = self.client.post(URL, json=payload)

                self.assertEqual(response.status_code, 422)
                # Virheellinen pyyntö ei saa päätyä kantaan
                self.assertEqual(self.get_saved_categories(), [])