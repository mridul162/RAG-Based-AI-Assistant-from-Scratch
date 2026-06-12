"""
main.py

Purpose:
--------
FastAPI application entrypoint for the
Hasanah Mart RAG system.

Responsibilities:
-----------------
- Create FastAPI application
- Register API routers
- Configure application metadata
- Initialize startup components

Architecture Philosophy:
------------------------
Single application entrypoint.

FastAPI
    ↓
Routers
    ↓
Services
    ↓
Repositories
    ↓
Database
"""

from fastapi import FastAPI

from api.core.config import (
    settings
)

from api.routes.chat import (
    router as chat_router
)


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

app.include_router(
    chat_router
)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }