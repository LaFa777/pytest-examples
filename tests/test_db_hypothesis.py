# thirdparty
import pytest
from hypothesis import given
from hypothesis.strategies import builds, text

# project
from src.fixtures import BasketItemFactory, UserFactory
from src.tables import Basket, BasketItem, User

# для интеграционных тестов надо создать контекст
from src.utils.sqlalchemy import get_session

pytestmark = pytest.mark.usefixtures("app_create")


@given(builds(UserFactory.build, username=text(max_size=12)))
def test_build_simple_user(user):
    assert isinstance(user, User)
    # казалось бы, этот ассерт должен сработать, но это не так!
    # hypotesis подсовывает в качестве предположения также пустую строку
    # assert user.username
    # а вот это уже сработает
    assert isinstance(user.username, str)

    # попробуем сохранить в базу
    session = get_session()
    session.add(user)

    # сбрасываем в транзакцию
    session.flush()

    users = session.query(User).all()
    assert users

    session.rollback()


@given(builds(BasketItemFactory.build, name=text()))
def test_build_heavy_fabric(basket_item):
    assert isinstance(basket_item, BasketItem)

    # попробуем сохранить в базу
    session = get_session()
    session.add(basket_item)

    # сбрасываем в транзакцию
    session.flush()

    # в базе должен быть 1 пользователь
    users = session.query(User).all()
    assert len(users) == 1
    # и 1 корзина
    basket = session.query(Basket).all()
    assert len(basket) == 1

    session.rollback()
