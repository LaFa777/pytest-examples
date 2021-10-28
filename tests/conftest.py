# thirdparty
import pytest
from pytest_factoryboy import register

# project
from app import app
from src import fixtures
from src.utils import sqlalchemy

register(fixtures.UserFactory)
register(fixtures.BasketFactory)
register(fixtures.BasketItemFactory)


@pytest.fixture(scope="session")
def app_create():
    # Исключаем ошибки фласка об отсутствии контекста
    ctx = app.app_context()
    ctx.push()


@pytest.fixture()
def sqlalchemy_session():
    session = sqlalchemy.get_session()

    yield session

    session.rollback()
    session.close()


@pytest.fixture()
def sqlalchemy_connection():
    connection = sqlalchemy.get_connection()

    yield connection

    connection.rollback()
    connection.close()


@pytest.fixture
def setup_factories(sqlalchemy_session):
    fixtures.UserFactory._meta.sqlalchemy_session = sqlalchemy_session
    fixtures.BasketFactory._meta.sqlalchemy_session = sqlalchemy_session
    fixtures.BasketItemFactory._meta.sqlalchemy_session = sqlalchemy_session
