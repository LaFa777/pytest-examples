# thirdparty
from faker import Faker
from sqlalchemy.orm import Session

# src
from .scenario import BaseScenario
from .user_scenario import UserScenario


class BasketScenario(BaseScenario):
    def __init__(self, user_scenario: UserScenario = None):
        self._user_scenario = user_scenario

    def insert_sql(self):
        return (
            "INSERT INTO basket (id, user_id, pickup) VALUES (:id, :user_id, :pickup) RETURNING id"
        )

    def generate_data(self, session: Session):
        user_ids = self._user_scenario.generate_to_db(session) if self._user_scenario else [None]

        for user_id in user_ids:
            yield {
                "id": Faker().pyint(),
                "pickup": Faker().pybool(),
                "user_id": user_id,
            }
