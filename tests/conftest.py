import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.database import SessionLocal
from app.models import Base


@pytest.fixture(scope='session')
def db():
    engine = create_engine('sqlite:///./test.db')
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    Base.metadata.create_all(engine)
    yield engine
    drop_database(engine.url)


@pytest.fixture
def db_session(db):
    # https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    connection = db.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()
