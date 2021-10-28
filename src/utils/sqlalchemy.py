# thirdparty
from flask import g
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session


def get_connection() -> Connection:
    if "db_engine_main" not in g:
        # thirdparty
        from flask import current_app as app

        # project
        from src.extensions import db

        g.db_engine_main = db.get_engine(app)  # noqa

    return Connection(engine=g.db_engine_main)


def get_session() -> Session:
    return Session(bind=get_connection())


def close_db(error):
    """Closes the db connections."""
    if "db_engine_main" in g:
        g.db_engine_main.dispose()
