from collections.abc import Callable
from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core import settings
from src.exceptions import TravelAgentError


# ------------------------------------------------------------------
# 🔧 Database config
# ------------------------------------------------------------------

DB_CONFIG = {
    "POOL_SIZE": settings["DB_POOL_SIZE"],
    "MAX_OVERFLOW": settings["DB_MAX_OVERFLOW"],
    "POOL_TIMEOUT": settings["DB_POOL_TIMEOUT"],
    "POOL_RECYCLE": settings["DB_POOL_RECYCLE"],
}


# ------------------------------------------------------------------
# 🧠 Lazy singleton caches
# ------------------------------------------------------------------

_engine_cache: dict[str, Engine] = {}
_sessionmaker_cache: dict[str, Callable[[], Session]] = {}


# ------------------------------------------------------------------
# 🔌 Engine factory (singleton per connection string)
# ------------------------------------------------------------------

def create_db_engine(
    db_conn_string: str,
    echo: bool = False,
    **kwargs: Any,
) -> Engine:
    """
    Create or return a cached SQLAlchemy engine.
    Engine is created ONLY once per connection string.
    """

    if db_conn_string in _engine_cache:
        return _engine_cache[db_conn_string]

    try:
        default_settings = {
            "pool_pre_ping": True,
            "pool_size": DB_CONFIG["POOL_SIZE"],
            "max_overflow": DB_CONFIG["MAX_OVERFLOW"],
            "pool_timeout": DB_CONFIG["POOL_TIMEOUT"],
            "pool_recycle": DB_CONFIG["POOL_RECYCLE"],
        }

        engine_settings = {**default_settings, **kwargs}

        engine = create_engine(
            db_conn_string,
            echo=echo,
            **engine_settings,
        )

        _engine_cache[db_conn_string] = engine
        return engine

    except Exception as e:
        raise TravelAgentError(
            message=str(e),
            error_code="DB_CONNECTION_FAILED",
            status_code=500,
        ) from e


# ------------------------------------------------------------------
# 🧵 Session factory (cached sessionmaker)
# ------------------------------------------------------------------

def create_db_session(
    engine: Engine,
    expire_on_commit: bool = True,
    autoflush: bool = False,
) -> Session:
    """
    Create or reuse a cached sessionmaker and return a Session.
    """

    try:
        cache_key = f"{engine.url}_{expire_on_commit}_{autoflush}"

        if cache_key not in _sessionmaker_cache:
            _sessionmaker_cache[cache_key] = sessionmaker(
                bind=engine,
                expire_on_commit=expire_on_commit,
                autoflush=autoflush,
            )

        SessionLocal = _sessionmaker_cache[cache_key]
        return SessionLocal()

    except Exception as e:
        raise TravelAgentError(
            message=str(e),
            error_code="DB_CONNECTION_FAILED",
            status_code=500,
        ) from e


# ------------------------------------------------------------------
# 🚀 Public entry point
# ------------------------------------------------------------------

def get_db_session() -> Session:
    """
    High-level DB session getter.
    Creates engine lazily and returns a session.
    """

    try:
        db_conn_string = settings["DATABASE_URL"]

        engine = create_db_engine(db_conn_string)
        session = create_db_session(engine)

        return session

    except Exception as e:
        raise TravelAgentError(
            message=str(e),
            error_code="DB_CONNECTION_FAILED",
            status_code=500,
        ) from e

