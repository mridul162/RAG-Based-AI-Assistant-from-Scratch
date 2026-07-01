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

from api.routers.chat import (
    router as chat_router
)

from api.routers.webhook import (
    router as webhook_router
)

from contextlib import asynccontextmanager

from api.database.base import Base
from api.database.session import engine

# IMPORTANT
from api.database.models.conversation import (
    ConversationMessageDB
)


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

app.include_router(
    chat_router
)

app.include_router(
    webhook_router
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