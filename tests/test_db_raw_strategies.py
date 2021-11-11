# stdlib
from typing import Optional

# thirdparty
from faker import Faker


class BaseScenario:
    def __init__(self, *args, **kwargs):
        pass

    def generate(self):
        raise NotImplementedError


class UserScenario(BaseScenario):
    def generate(self):
        return {
            "id": Faker.pyint(),
            "username": Faker.first_name(),
        }


class BasketScenario(BaseScenario):
    def __init__(self, user_scenario: Optional[BaseScenario] = None):
        self._user_scenario = user_scenario

    def generate(self):
        return {
            "id": Faker.pyint(),
            "user": self._user_scenario.generate()["id"],
            "pickup": Faker.pybool(),
        }
