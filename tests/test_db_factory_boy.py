"""
Пример с тестов на библиотеке Factory Boy
"""
# thirdparty
import pytest

# project
from src import fixtures
from src.tables import Basket, BasketItem, User  # noqa

# для интеграционных тестов надо создать контекст
pytestmark = pytest.mark.usefixtures("app_create", "setup_factories")


def test_create_user(sqlalchemy_session, user):
    """
    :param user: экземпляр tables.User
    """
    user_db = sqlalchemy_session.query(User).first()
    assert user_db == user


def test_create_user_with_custom_name(sqlalchemy_session, user_factory):
    """
    :param user_factory: фабрика fixtures.UserFactory
    """
    user = user_factory(username="Павел")

    user_db = sqlalchemy_session.query(User).first()
    assert user_db.username == user.username


def test_create_basket(sqlalchemy_session, basket, user):
    """
    :param basket: инстанс tables.Basket
    """
    basket_db = sqlalchemy_session.query(Basket).first()
    assert basket_db == basket
    assert basket_db.user == user


def test_create_basket_item(sqlalchemy_session):
    item = fixtures.BasketItemFactory()

    basket_item_db = sqlalchemy_session.query(BasketItem).first()
    assert basket_item_db == item
    assert basket_item_db.price == item.price
