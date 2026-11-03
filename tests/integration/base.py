
import os
import unittest
from pathlib import Path

from alembic.config import Config
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from alembic import command
from db import get_db
from main import app

# Projektin juurikansio, jotta tiedostot löytyvät riippumatta siitä, mistä testit ajetaan
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class IntegrationTestCase(unittest.TestCase):
    """Yhteinen pohjaluokka integraatiotesteille: tarkistetaan, ettei testejä vahingossa ajeta oikeaa tietokantaa vasten """

    @classmethod
    def setUpClass(cls):
        # override=True, jotta .env.test yliajaa jo ladatun .env:n.
        # CI:ssä tiedostoa ei ole, jolloin käytetään workflow'n DATABASE_URL-muuttujaa
        load_dotenv(PROJECT_ROOT / ".env.test", override=True)
        database_url = os.getenv("DATABASE_URL", "")

        # Integraatiotestit tyhjentävät taulut, joten niitä ei saa ajaa kehityskantaa vasten.
        # DATABASE_URL:n pitää osoittaa kantaan, jonka nimi päättyy _test (esim. lainaamo_test)
        cls.engine = create_engine(database_url)
        database = cls.engine.url.database or ""
        if not database.endswith("_test"):
            raise RuntimeError(
                f"Integraatiotestit vaativat testikannan (nimi päättyy _test), nyt: '{database}'"
            )

        # Sama kuin ajaisi komentoriviltä: alembic upgrade head
        command.upgrade(Config(PROJECT_ROOT / "alembic.ini"), "head")

        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

        # db.py loi oman enginensä jo importattaessa .env:n osoitteella, joten pelkkä
        # .env.test ei riitä. Korvataan sovelluksen get_db-riippuvuus niin, että myös
        # API-kutsut käyttävät testikantaa
        def get_test_db():
            db = cls.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = get_test_db

        # TestClient lähettää HTTP-pyynnöt suoraan sovellukselle ilman erillistä palvelinta.
        # enterClassContext sulkee clientin automaattisesti, kun luokan testit on ajettu
        cls.client = cls.enterClassContext(TestClient(app))

    @classmethod
    def tearDownClass(cls):
        # Palautetaan sovelluksen oikea get_db ja suljetaan tietokantayhteydet
        app.dependency_overrides.pop(get_db, None)
        cls.engine.dispose()

    def setUp(self):
        # Jokainen testi alkaa tyhjästä taulusta, jotta testit eivät vaikuta toisiinsa
        # eivätkä ole ajojärjestyksestä riippuvia. Siivous tehdään ennen testiä, jotta
        # kesken kaatunut ajo ei jätä rivejä seuraavalle. RESTART IDENTITY nollaa id-laskurin
        with self.engine.begin() as connection:
            connection.execute(text("TRUNCATE TABLE categories RESTART IDENTITY CASCADE"))

        # Testin oma sessio, jolla luetaan kannasta mitä sinne oikeasti tallentui
        self.session = self.SessionLocal()

    def tearDown(self):
        self.session.close()