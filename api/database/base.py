"""
base.py

Purpose:
--------
SQLAlchemy declarative base for all
database models.

Responsibilities:
-----------------
- Provide a common ORM base class
- Register model metadata

Architecture Philosophy:
------------------------
Single source of truth.
Minimal ORM foundation.
"""

from sqlalchemy.orm import (
    DeclarativeBase
)


# ---------------------------------------------------------
# DECLARATIVE BASE
# ---------------------------------------------------------

class Base(DeclarativeBase):

    """
    Base class for all ORM models.
    """

    pass