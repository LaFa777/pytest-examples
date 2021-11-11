# thirdparty
from faker import Faker
from sqlalchemy.orm import Session

# project
from tests.raw_scenarios.scenario import BaseScenario


class UserScenario(BaseScenario):
    def insert_sql(self):
        return "INSERT INTO user (id, username) VALUES (:id, :username) RETURNING id"

    def generate_data(self, session: Session):
        yield {
            "id": Faker().pyint(min_value=0, max_value=9999999),
            "username": Faker().first_name(),
        }


class MultipleUserScenario(UserScenario):
    def __init__(self, num: int):
        self._num_generate = num

    def generate_data(self, session: Session):
        for _ in range(self._num_generate):
            yield next(super().generate_data(session))
