"""
session.py

Purpose:
--------
Database engine and session management
for the Hasanah Mart AI assistant.

Responsibilities:
-----------------
- Create database engine
- Create session factory
- Provide database sessions

Architecture Philosophy:
------------------------
Single engine.
Reusable sessions.
Dependency-injection friendly.
"""

from collections.abc import Generator

from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import (
    Session,
    sessionmaker
)

from api.core.config import (
    settings
)


# ---------------------------------------------------------
# DATABASE ENGINE
# ---------------------------------------------------------

engine = create_engine(

    settings.database_url,

    pool_pre_ping=True
)


# ---------------------------------------------------------
# SESSION FACTORY
# ---------------------------------------------------------

SessionLocal = sessionmaker(

    bind=engine,

    autoflush=False,

    autocommit=False,

    expire_on_commit=False
)


# ---------------------------------------------------------
# DATABASE DEPENDENCY
# ---------------------------------------------------------

def get_db() -> Generator[
    Session,
    None,
    None
]:
    """
    Provide a database session.

    Usage:
        db = next(get_db())
    """

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()