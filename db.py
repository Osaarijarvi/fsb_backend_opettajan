
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# postgresql+psycopg2://postgres:salasana@localhost:5435/lainaamo
DATABASE_URL = os.getenv('DATABASE_URL', "")

# engine luodaan kerran koko sovelluksen eliniäksi
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kaikki model-luokat perivät tämän

# tämä on issuen korjaus
# tämä on issuen korjaus
# tämä on issuen korjaus
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()