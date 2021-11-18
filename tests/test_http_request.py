# для интеграционных тестов надо создать контекст
# thirdparty
import pytest
from mock import patch

pytestmark = pytest.mark.usefixtures("app_create", "setup_factories")


def test_home_page(test_client):
    response = test_client.get("/pytest/hello")

    assert response.status_code == 200
    assert response.data.decode() == "Hello pytest :)"


def test_get_username(sqlalchemy_session, test_client, user):
    # в файле произошел импорт метода get_session, поэтому нужно указать так
    # т.е. patch("src.utils.sqlalchemy.get_session") тут не сработает
    with patch("src.views.get_session") as session_mock:
        session_mock.return_value = sqlalchemy_session
        response = test_client.get(f"/pytest/user/{user.id}/username")

    assert response.status_code == 200
    assert response.data.decode() == user.username
