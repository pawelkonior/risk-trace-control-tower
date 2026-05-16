from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool, StaticPool

DEFAULT_DATABASE_URL = "sqlite+pysqlite:///:memory:"


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models used by RiskTrace APIs."""


SessionFactory = sessionmaker[Session]


def database_url_from_env() -> str:
    """Resolve the database URL used by REST-facing RiskTrace APIs."""
    return os.getenv("RWA_DATABASE_URL", DEFAULT_DATABASE_URL)


def create_database_engine(database_url: str | None = None) -> Engine:
    """Create an SQLAlchemy engine with test-friendly SQLite handling."""
    resolved_url = database_url or os.getenv("RWA_DATABASE_URL")
    if resolved_url is None:
        sqlite_path = Path(gettempdir()) / f"risktrace-ui-{uuid4().hex}.sqlite3"
        resolved_url = f"sqlite+pysqlite:///{sqlite_path}"
    if resolved_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        if resolved_url.endswith(":memory:"):
            return create_engine(
                resolved_url,
                connect_args=connect_args,
                poolclass=StaticPool,
                future=True,
            )
        return create_engine(
            resolved_url,
            connect_args=connect_args,
            poolclass=NullPool,
            future=True,
        )
    return create_engine(resolved_url, pool_pre_ping=True, future=True)


def create_session_factory(engine: Engine) -> SessionFactory:
    """Create a session factory for FastAPI dependencies and service tests."""
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def session_scope(session_factory: SessionFactory) -> Generator[Session]:
    """Yield a request-scoped DB session."""
    with session_factory() as session:
        yield session
