# thirdparty
import pytest

# project
from src.tables import Basket, BasketItem, User  # noqa

# для интеграционных тестов надо создать контекст
pytestmark = pytest.mark.usefixtures("app_create")


def test_create_user(sqlalchemy_session, mixer):
    mixed_user = mixer.blend(User)  # type: User
    db_user = sqlalchemy_session.query(User).first()

    assert db_user.username == mixed_user.username
