# thirdparty
from faker import Faker
from sqlalchemy.orm import Session

# project
from tests.raw_scenarios.basket_scenario import BasketScenario
from tests.raw_scenarios.scenario import BaseScenario


class BasketItemScenario(BaseScenario):
    def __init__(self, basket_scenario: BasketScenario = None):
        self._basket_scenario = basket_scenario

    def insert_sql(self):
        return (
            "INSERT INTO basket_item (id, name, price, basket_id) "
            "VALUES (:id, :name, :price, :basket_id) RETURNING id"
        )

    def generate_data(self, session: Session):
        basket_ids = (
            self._basket_scenario.generate_to_db(session) if self._basket_scenario else [None]
        )

        for basket_id in basket_ids:
            yield {
                "id": Faker().pyint(),
                "name": Faker(locale="ru").sentence(nb_words=3),
                # товары в нашем магазине очень дорогие
                "price": Faker().random_int(min=999, max=2999),
                "basket_id": basket_id,
            }
