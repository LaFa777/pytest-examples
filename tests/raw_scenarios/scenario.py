# stdlib
from typing import List

# thirdparty
from sqlalchemy.orm import Session


class IScenario:
    """
    Интерфейс для описания сценариев генерации данных
    """

    def insert_sql(self):
        """
        Абстрактный метод.

        Печка подсвечивает, что в родителях не реализованы методы с NotImplementedError
        """
        raise NotImplementedError

    def generate_data(self, session: Session):
        raise NotImplementedError


class BaseScenario(IScenario):
    """
    А это уже абстрактный класс
    """

    def _init_obj(self):
        """
        Внимание! Тут пример плохого "библиотечного кода"! Никогда не делайте так :)

        Само собой этот метод можно реализовать в __init__, но тогда всем наследникам нужно будет
        его вызывать.
        """
        if not hasattr(self, "_generated_objects"):
            self._generated_objects = []

    def generate_to_db(self, session: Session) -> List[int]:
        """
        :rtype: список вставленных в базу id объектов
        """
        self._init_obj()

        insert_sql = self.insert_sql()

        # в случае, если у нас много данных, то вставить должны мы их все
        inserted_ids = []
        for data in self.generate_data(session):
            result_proxy = session.execute(insert_sql, data)

            # получение значений
            result = result_proxy.first()
            user_id = result[0]

            # вдруг кому нибудь потом понадобятся записанные в базу данные
            self._generated_objects.append(data)

            inserted_ids.append(user_id)

        return inserted_ids

    def get_generated_objects(self):
        return self._generated_objects
