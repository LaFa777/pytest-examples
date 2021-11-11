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

    transaction = connection.begin()
    yield connection
    transaction.rollback()
    transaction.close()

    connection.close()


@pytest.fixture
def setup_factories(sqlalchemy_session):
    fixtures.UserFactory._meta.sqlalchemy_session = sqlalchemy_session
    fixtures.BasketFactory._meta.sqlalchemy_session = sqlalchemy_session
    fixtures.BasketItemFactory._meta.sqlalchemy_session = sqlalchemy_session


@pytest.fixture
def mixer(sqlalchemy_connection):
    # thirdparty
    from mixer.backend.flask import Mixer

    no_commit_mixer = Mixer(commit=False)
    no_commit_mixer.init_app(app)

    yield no_commit_mixer


@pytest.fixture
def test_client():
    """
    Фикстура для тестирования вьюх
    """
    test_client = app.test_client()
    yield test_client
