"""
Пример с тестов на алхимии
"""
# thirdparty
import pytest

# project
from src.tables import Basket, BasketItem, User  # noqa

# для интеграционных тестов надо создать контекст
pytestmark = pytest.mark.usefixtures("app_create")


def test_create_basket_with_items(sqlalchemy_session):
    user = User(
        username="Кирилл",
        baskets=[
            Basket(
                pickup=False,
                items=[
                    BasketItem(name="Яблоко", price=64),
                    BasketItem(name="Хлеб", price=12),
                    BasketItem(name="Колбаса", price=120),
                ],
            )
        ],
    )
    # Сохраняем в базу
    sqlalchemy_session.merge(user)

    # #### В базу сохранили, теперь проверяем, что мы не наврали.

    basket = sqlalchemy_session.query(Basket).first()

    assert basket
