import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.database import SessionLocal
from app.models import Base


@pytest.fixture
def setup_db():
    engine = create_engine('sqlite:///./test.db')
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    Base.metadata.create_all(engine)
    SessionLocal.configure(bind=engine)
    yield
    drop_database(engine.url)


@pytest.fixture
def db_session(setup_db):
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
