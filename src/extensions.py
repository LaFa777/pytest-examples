# thirdparty
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# project
from src.utils import sqlalchemy

db: SQLAlchemy = SQLAlchemy()


def sqlalchemy_init(app):
    global db
    db.init_app(app)
    app.teardown_appcontext(sqlalchemy.close_db)

    # инициализируем миграции
    Migrate(app, db)
