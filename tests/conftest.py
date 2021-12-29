from typing import List

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.database import SessionLocal
from app.models import Base, User
from app.repositories import ProjectRepository, UserRepository


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


@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)


@pytest.fixture
def user(user_repository) -> User:
    user = User(first_name='user', email='user@mail.com')
    return user_repository.add(user)


@pytest.fixture
def users(user_repository) -> List[User]:
    user1 = User(first_name='user1', email='user1@mail.com', is_superuser=True)
    user2 = User(first_name='user2', email='user2@mail.com', is_superuser=True)
    user3 = User(first_name='user3', email='user3@mail.com')
    return [
        user_repository.add(user1),
        user_repository.add(user2),
        user_repository.add(user3),
    ]


@pytest.fixture
def project_repository(db_session):
    return ProjectRepository(db_session)
