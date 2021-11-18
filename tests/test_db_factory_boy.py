"""
Пример с тестов на библиотеке Factory Boy
"""
# stdlib
import random

# thirdparty
import pytest

# project
from src import fixtures
from src.tables import Basket, BasketItem, User  # noqa
from src.utils.sqlalchemy import get_session

# для интеграционных тестов надо создать контекст
pytestmark = pytest.mark.usefixtures("app_create", "setup_factories")


def test_create_user_with_factory(sqlalchemy_session):
    # создадим пользователя со случайно заполненными данными
    # и под капотом сохранияем его в транзакцию
    user = fixtures.UserFactory(username="Хасбик")

    # в рамках транзакции все должно быть в базе
    user_db = sqlalchemy_session.query(User).first()
    assert user == user_db
    assert user_db.username == user.username

    # а давайте попробуем проверить меня на честность и создадим еще одну транзакцию.
    # В базе рыли должно быть пусто
    new_sqlalchemy_session = get_session()
    users = new_sqlalchemy_session.query(User).all()
    assert not users


def test_build_user_without_save(sqlalchemy_session, user_factory):
    # создаем пользователя без сохранения в базу
    narko_user = user_factory.build(username="Волтер Уайт")
    assert isinstance(narko_user, User)
    assert narko_user.username == "Волтер Уайт"

    # проверяем, что база действительно пустая
    users = sqlalchemy_session.query(User).all()
    assert not users
    # вау! неожиданно! она пустая!!! :O
    #

    #
    # хм, не, я передумал. Давайте сохраним в базу
    sqlalchemy_session.add(narko_user)

    # изменения в базе не появятся, пока мы не закоммитим или не сбросим буфер в базу
    # sqlalchemy_session.commit() <- НЕ ВЕРНО!!!
    sqlalchemy_session.flush()

    # проверяем, что в базе что то появилось
    users = sqlalchemy_session.query(User).all()
    assert users
    # вау! неожиданно! она НЕ пустая!!! :)


def test_create_user_with_save(sqlalchemy_session, user_factory):
    # создадим еще одного покупателя в нашем магазине
    yet_another_narko_user = user_factory.create(username="Джесси Пинкман")

    # вроде бы, он должен появиться в базе (я не уверен, но в доке было написано так)
    users = sqlalchemy_session.query(User).all()
    # этот тест ограничен транзакцией, так что я думаю пользователь должен быть всего один
    assert len(users) == 1
    jeccy = users[0]
    assert jeccy == yet_another_narko_user


def test_create_user(sqlalchemy_session, user):
    """
    :param user: экземпляр tables.User, уже созданный в базе (без коммита транзакции)
    """
    # может описание обмануло? это точно созданный пользователь?
    assert isinstance(user, User)

    # хм. И в базе что ли появилось?
    user_db = sqlalchemy_session.query(User).first()
    assert user_db == user


def test_create_user_with_custom_name(sqlalchemy_session, user_factory):
    # просто тоже самое, что и .create()
    user = user_factory(username="Чимс")

    # и работает также
    user_db = sqlalchemy_session.query(User).first()
    assert user_db.username == user.username


def test_create_basket(sqlalchemy_session, basket, user):
    """
    Сгенерируем корзину. (типа пользователь сделал покупку)
    """
    # проверяем что в базе действительно создалась корзина
    basket_db = sqlalchemy_session.query(Basket).first()
    assert basket_db == basket

    # так стопэ, корзину же оформляет кто то?
    # так он у нас связан через фикстуру :)
    assert basket_db.user == user


def test_create_basket_item_as_bulba(sqlalchemy_session):
    # так, создадим товар в корзине!
    item = fixtures.BasketItemFactory(name="Бульба free", price=1.5)

    basket_item_db = sqlalchemy_session.query(BasketItem).first()
    # у нашей картошечки должна быть цена!
    assert basket_item_db.price == item.price


def test_create_user_with_factory_trait(sqlalchemy_session):
    # а вот тут нам нужно, чтобы пользователь был обязательно сгенерирован с нужными нам данными.
    # На самом деле не особо нужно... это просто пример :(
    muscled_doge = fixtures.UserFactory(doge=True)
    assert muscled_doge.username == "Качок доге"

    user_db = sqlalchemy_session.query(User).first()
    assert muscled_doge == user_db


def test_create_multiple_baskets_with_one_user(
    sqlalchemy_session, user_factory, basket_factory, basket_item_factory
):
    # что-то не хочется базу нагружать. Потом сохраним в базу.
    rich_chel = user_factory.build(username="Богатый чел 😎 очень богатый 💴 💴 💴")

    for _ in range(10):
        # а тут я захотел сразу сохранить в базу
        rich_basket = basket_factory.create(user=rich_chel)
        # в каждой корзинке должно быть хотя бы несколько товаров (а может и не быть)
        for _ in range(random.randint(0, 10)):
            basket_item_factory(basket=rich_basket)

    baskets = sqlalchemy_session.query(Basket).all()
    assert len(baskets) == 10
