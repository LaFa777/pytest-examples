"""
Конфиг для запуска тестов
"""
# project
from settings.base import *  # noqa

SQLALCHEMY_DATABASE_URI = "sqlite:///dbs/pytests.db"
