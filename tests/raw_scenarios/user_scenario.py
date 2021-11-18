# thirdparty
from faker import Faker
from sqlalchemy.orm import Session

# project
from tests.raw_scenarios.scenario import BaseScenario


def get_uniq_num():
    get_uniq_num.start_num += 1
    return get_uniq_num.start_num


get_uniq_num.start_num = Faker().pyint(min_value=0, max_value=999)


class UserScenario(BaseScenario):
    def insert_sql(self):
        return "INSERT INTO user (id, username) VALUES (:id, :username) RETURNING id"

    def generate_data(self, session: Session):
        yield {
            "id": get_uniq_num(),
            # т.к. у нас уникальный ключ по username, то мы не можем гарантировать уникальной
            # значений следующей строкой
            # "username": Faker().first_name(),
            # а так можем
            "username": Faker().uuid4(),
        }


class MultipleUserScenario(UserScenario):
    def __init__(self, num: int):
        self._num_generate = num

    def generate_data(self, session: Session):
        for _ in range(self._num_generate):
            yield next(super().generate_data(session))
