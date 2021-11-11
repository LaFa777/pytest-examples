"""
Пример с тестов на библиотеке Factory Boy
"""
# thirdparty
import pytest

# project
from src.repositories.raw_repository import RawRepository
from src.tables import Basket, BasketItem, User  # noqa

# для интеграционных тестов надо создать контекст
pytestmark = pytest.mark.usefixtures("app_create")


@pytest.fixture
def sql_user_insert():
    return "INSERT INTO user (username) VALUES (?) RETURNING user.id"


@pytest.mark.parametrize("username", ["Кирилл", "Валера", "Другой Кирилл"])
def test_create_user(sqlalchemy_connection, sql_user_insert, username):
    # запись в базу
    result_proxy = sqlalchemy_connection.execute(sql_user_insert, username)
    # получение значений
    result = result_proxy.first()
    user_id = result[0]

    # смотрим, что в базу записалось все
    username_from_db = RawRepository(sqlalchemy_connection).get_username(user_id)

    assert username == username_from_db


@pytest.fixture
def sql_insert_user_kirill(sqlalchemy_connection, sql_user_insert):
    username = "Кирилл"
    # запись в базу
    result_proxy = sqlalchemy_connection.execute(sql_user_insert, username)
    # получение значений
    result = result_proxy.first()
    user_id = result[0]

    return user_id, username


def test_create_user_with_fixture_kirill(sqlalchemy_connection, sql_insert_user_kirill):
    user_id = sql_insert_user_kirill[0]
    username = sql_insert_user_kirill[1]

    # смотрим, что в базу записалось все
    username_from_db = RawRepository(sqlalchemy_connection).get_username(user_id)

    assert username == username_from_db
