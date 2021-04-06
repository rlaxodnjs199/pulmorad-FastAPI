from functools import lru_cache
from contextlib import contextmanager
from typing import Iterator, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker as sa_sessionmaker
from sqlalchemy.engine import Engine as sa_engine

from app import config


class FastAPISessionMaker:
    def __init__(self, database_uri: str):
        self.database_uri = database_uri
        self._cached_engine: Optional[sa_engine] = None
        self._cached_sessionmaker: Optional[sa_sessionmaker] = None

    @property
    def cached_engine(self) -> sa_engine:
        engine = self._cached_engine
        if engine is None:
            print("Initiating Postgresql Engine")
            engine = self.get_new_engine()
            self._cached_engine = engine
        return engine

    @property
    def cached_sessionmaker(self) -> sa_sessionmaker:
        sessionmaker = self._cached_sessionmaker
        if sessionmaker is None:
            print("Initiating Postgresql Session")
            sessionmaker = self.get_new_sessionmaker()
            self._cached_sessionmaker = sessionmaker
        return sessionmaker

    def get_new_engine(self) -> sa_engine:
        return get_engine(self.database_uri)

    def get_new_sessionmaker(self, engine: Optional[sa_engine] = None) -> sa_sessionmaker:
        engine = engine or self.cached_engine
        return get_sessionmaker_for_engine(engine)

    @contextmanager
    def context_session(self) -> Iterator[Session]:
        yield from self.get_db()

    def get_db(self) -> Iterator[Session]:
        yield from _get_db(self.cached_sessionmaker)

    def reset_cache(self) -> None:
        self._cached_engine = None
        self._cached_sessionmaker = None


def get_engine(db_uri: str) -> sa_engine:
    return create_engine(db_uri, pool_pre_ping=True)


def get_sessionmaker_for_engine(engine: sa_engine) -> sa_sessionmaker:
    return sa_sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def context_session(engine: sa_engine) -> Iterator[Session]:
    sessionmaker = get_sessionmaker_for_engine(engine)
    yield from _get_db(sessionmaker)


def _get_db(sessionmaker: sa_sessionmaker) -> Iterator[Session]:
    session = sessionmaker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise Exception
    finally:
        session.close()


@lru_cache
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    db_uri = str(config.DATABASE_URL)
    return FastAPISessionMaker(db_uri)


def get_db() -> Iterator[Session]:
    yield from _get_fastapi_sessionmaker().get_db()
