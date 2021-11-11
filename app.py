# stdlib
import os

# thirdparty
from flask import Flask

# project
from src import extensions
from src.tables import *  # noqa
from src.views import pytest_routes

app = Flask(__name__)

# считываем конфиг
environ = "dev"
if os.environ.get("STAGE"):
    environ = os.environ["STAGE"].lower()
app.config.from_pyfile(f"settings/{environ}.py")


# регистрируем расширения
def register_extensions(app):
    extensions.sqlalchemy_init(app)

    # штуки для разработчиков запускаем только под dev окружением
    if app.config["DEBUG"]:
        pass


register_extensions(app)

# регистрируем view
app.register_blueprint(pytest_routes)
