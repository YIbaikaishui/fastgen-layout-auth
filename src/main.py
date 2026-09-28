"""FastAPI application entrypoint.

Module routers are loaded automatically from the registry
(``src.modules``), so adding a module via ``fastgen make module``
requires no edits here.
"""

from __future__ import annotations

import importlib
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.database import engine
from src.modules import modules


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Schema is managed by Alembic: `uv run alembic upgrade head`.
    yield
    await engine.dispose()


app = FastAPI(title="FastAPI Auth Layout (fastgen)", version="0.1.0", lifespan=lifespan)

# --- fastgen: auto-mount (do not remove) ---
for _import_path in modules.values():
    _module = importlib.import_module(_import_path)
    app.include_router(_module.router)
# --- fastgen: end auto-mount ---


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
