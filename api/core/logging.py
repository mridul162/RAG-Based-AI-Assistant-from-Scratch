"""
logging.py

Purpose:
--------
Centralized logging configuration for the
Hasanah Mart multilingual RAG system.

Responsibilities:
-----------------
- Console logging
- Rotating file logging
- Unified logger creation
- UTF-8 safe logging
- Production-friendly formatting

Architecture Philosophy:
------------------------
Centralized observability.
Readable structured logs.
Deployment-friendly logging.
"""

import logging
import sys

from pathlib import Path

from logging.handlers import (
    RotatingFileHandler
)

from api.core.config import (
    PROJECT_ROOT
)


# ---------------------------------------------------------
# LOG DIRECTORY
# ---------------------------------------------------------

LOG_DIR = (
    PROJECT_ROOT / "logs"
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = (
    LOG_DIR / "app.log"
)


# ---------------------------------------------------------
# LOG FORMAT
# ---------------------------------------------------------

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = (
    "%Y-%m-%d %H:%M:%S"
)


# ---------------------------------------------------------
# SETUP LOGGING
# ---------------------------------------------------------

def setup_logging():

    """
    Configure application-wide logging.
    """

    root_logger = logging.getLogger()

    # -------------------------------------------------
    # Prevent duplicate handlers
    # -------------------------------------------------

    if root_logger.handlers:

        return

    root_logger.setLevel(
        logging.INFO
    )

    formatter = logging.Formatter(

        fmt=LOG_FORMAT,

        datefmt=DATE_FORMAT,
    )

    # -------------------------------------------------
    # Console Handler
    # -------------------------------------------------

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setFormatter(
        formatter
    )

    # -------------------------------------------------
    # Rotating File Handler
    # -------------------------------------------------

    file_handler = RotatingFileHandler(

        filename=LOG_FILE,

        encoding="utf-8",

        maxBytes=5 * 1024 * 1024,

        backupCount=5,
    )

    file_handler.setFormatter(
        formatter
    )

    # -------------------------------------------------
    # Attach Handlers
    # -------------------------------------------------

    root_logger.addHandler(
        console_handler
    )

    root_logger.addHandler(
        file_handler
    )

    # -------------------------------------------------
    # Reduce noisy third-party logs
    # -------------------------------------------------

    logging.getLogger(
        "httpx"
    ).setLevel(logging.WARNING)

    logging.getLogger(
        "openai"
    ).setLevel(logging.WARNING)

    logging.getLogger(
        "uvicorn.access"
    ).setLevel(logging.INFO)

    logging.getLogger(
        "urllib3"
    ).setLevel(logging.WARNING)

    root_logger.info(
        "Logging initialized."
    )


# ---------------------------------------------------------
# LOGGER FACTORY
# ---------------------------------------------------------

def get_logger(
    name: str
) -> logging.Logger:

    """
    Create module-level logger.
    """

    return logging.getLogger(name)