# thirdparty
import pytest
from sqlalchemy.orm import Session

# project
from src import tables
from tests.raw_scenarios.basket_item_scenario import BasketItemScenario
from tests.raw_scenarios.basket_scenario import BasketScenario
from tests.raw_scenarios.user_scenario import MultipleUserScenario, UserScenario

# для интеграционных тестов надо создать контекст
pytestmark = pytest.mark.usefixtures("app_create")


def test_user_scenario(sqlalchemy_session):
    scenario = UserScenario()

    # записываем в базу
    user_ids = scenario.generate_to_db(sqlalchemy_session)

    # в базе должен существовать наш пользователь
    assert sqlalchemy_session.query(tables.User).filter(tables.User.id == user_ids[0]).first()


def test_multiple_user_scenario(sqlalchemy_session):
    scenario = MultipleUserScenario(num=10)

    # записываем в базу
    scenario.generate_to_db(sqlalchemy_session)

    # 1. проверяем, что мы записали 10 пользователей
    assert sqlalchemy_session.query(tables.User).count()

    # 2. а давайте проверим, что созданные пользователи действительно есть в базе
    users = scenario.get_generated_objects()
    for user in users:
        user_id = user["id"]
        assert sqlalchemy_session.query(tables.User).filter(tables.User.id == user_id).first()


def get_basket_item_name(session: Session, basket_item_id: int):
    sql_select_item_name = "SELECT name FROM basket_item WHERE id = :item_id"
    result_proxy = session.execute(sql_select_item_name, {"item_id": basket_item_id})
    result = result_proxy.first()
    db_item_name = result[0]
    return db_item_name


def test_basket_item(sqlalchemy_session):
    basket_item = BasketItemScenario(basket_scenario=BasketScenario(user_scenario=UserScenario()))
    basket_item.SESSION = sqlalchemy_session
    basket_item_ids = basket_item.generate_to_db(sqlalchemy_session)
    basket_item_id = basket_item_ids[0]

    basket_item_data = basket_item.get_generated_objects()
    item_name = basket_item_data[0]["name"]

    # проверяем, что мы действительно записали в базу
    db_item_name = get_basket_item_name(sqlalchemy_session, basket_item_id)

    assert db_item_name == item_name
