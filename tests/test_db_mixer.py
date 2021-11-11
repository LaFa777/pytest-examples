# thirdparty
import pytest

# project
from src.tables import Basket, BasketItem, User  # noqa

# для интеграционных тестов надо создать контекст
pytestmark = pytest.mark.usefixtures("app_create")


# mixer это фикстура!
def test_create_user(sqlalchemy_session, mixer):
    # Рандомим параметры Пользователя
    mixed_user = mixer.blend(User)  # type: User

    # Добавляем пользователя в базу
    sqlalchemy_session.add(mixed_user)

    db_user = sqlalchemy_session.query(User).first()

    assert db_user.username == mixed_user.username
