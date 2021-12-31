from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.config import settings
from app.database import SessionLocal, generate_db_session
from app.main import app
from app.models import Base, Project, User
from app.repositories import ProjectRepository, UserRepository
from app.services import UserService


@pytest.fixture(scope='session')
def db():
    engine = create_engine(
        'sqlite:///./test.db',
        connect_args={'check_same_thread': False},
    )
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
def client(db_session):
    app.dependency_overrides[generate_db_session] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def user_repository(db_session):
    return UserRepository(db_session)


@pytest.fixture
def user(user_repository) -> User:
    user = User(
        first_name='user',
        email='user@mail.com',
        password='123456',  # type: ignore
    )
    return user_repository.add(user)


@pytest.fixture
def inactive_user(user_repository) -> User:
    user = User(
        email='user@mail.com',
        password='123456',  # type: ignore
        is_active=False,
    )
    return user_repository.add(user)


@pytest.fixture
def superuser(user_repository) -> User:
    user = User(
        email=settings.DEFAULT_SUPERUSER_EMAIL,
        password='123456',  # type: ignore
        is_superuser=False,
    )
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


@pytest.fixture
def project(project_repository, user) -> Project:
    project = Project(
        title='Project1',
        description='My project',
        url='myproject.com',
        owner_id=user.id,
    )
    return project_repository.add(project)


@pytest.fixture
def projects(project_repository, users) -> List[Project]:
    project1 = Project(
        title='Project1',
        description='My First project',
        url='http://myproject1.com',
        owner_id=users[0].id,
    )
    project2 = Project(
        title='Project1',
        description='My Second project',
        url='http://myproject2.com',
        owner_id=users[1].id,
    )
    project3 = Project(
        title='Project3',
        description='My Third project',
        url='http://myproject3.com',
        owner_id=users[1].id,
    )
    return [
        project_repository.add(project1),
        project_repository.add(project2),
        project_repository.add(project3),
    ]


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)
