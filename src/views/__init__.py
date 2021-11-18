# thirdparty
from flask import Blueprint, make_response

# project
from src import tables
from src.utils.sqlalchemy import get_session

pytest_routes = Blueprint("pytest_routes", __name__)


@pytest_routes.route("/pytest/hello")
def pytest_hello():
    response = make_response("Hello pytest :)", 200)
    response.mimetype = "text/plain"
    return response


@pytest_routes.route("/pytest/user/<id>/username")
def get_username(id):
    session = get_session()
    user = session.query(tables.User).filter(tables.User.id == id).first()
    return user.username
