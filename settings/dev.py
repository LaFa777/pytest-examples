# project
from settings.base import *  # noqa

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///dbs/app.db"

# для импорта локальной конфигурации
try:
    # project
    from settings.local import *  # noqa
except Exception:
    pass
