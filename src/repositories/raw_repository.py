# thirdparty
import sqlalchemy.engine


class RawRepository:
    _SQL_SELECT_USERNAME = "SELECT username FROM user WHERE id = ?"

    def __init__(self, connection: sqlalchemy.engine.Connection):
        self._connection = connection

    def get_username(self, user_id: int):
        result_proxy = self._connection.execute(self._SQL_SELECT_USERNAME, user_id)
        result = result_proxy.first()
        username_from_db = result[0]
        return username_from_db
