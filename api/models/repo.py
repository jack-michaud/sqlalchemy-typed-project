from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

import api.config


from api import app


class BaseModel:
    @property
    def id(self):
        return 1

    @id.setter
    def id(self, value):
        raise NotImplementedError()


# Probably more structured and useful ways to do this
def default_db_session() -> Session:
    engine = create_engine(app.config["DATABASE_URL"])
    return sessionmaker(bind=engine)()


class Repo:

    # Parameterizing db_session makes it easy to swap between, say, primaries and read-replicas
    # It makes mocking out the entire db in unit tests simpler with a mocked db_session object
    # Finally, it lets the repo own certain leaky db_session semantics like flushing or resetting
    #  failed transactions if it needs to. ie: we could add contextmanager functions here that do teardown.
    def __init__(self, db_session: Optional[Session]):
        self.db_session = db_session or default_db_session()

    # Then we can wrap all direct db_session calls. These are not meant to be used in application code,
    # but can be used in higher-level model class functions, demonstrated a little later

    # querying: return a chainable query object
    # then can do, say:
    # - repo.query(User).order_by(User.id).all()
    # - repo.query(User, User.name).order_by(User.name).first()
    def query(self, *args) -> Query:
        return self.db_session.query(*args)

    # insertion update would work similarly, however note that
    # session cleanup and transaction cleanup mechanisms and APIs vary wildly
    # between versions of sqlalchemy, read the docs carefully!
    def insert(self, record: BaseModel):
        with self.db_session.begin(), self.db_session.transaction:
            self.db_session.add(record)
        self.db_session.commit()
