from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.core.config import get_settings

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(api_router, prefix=settings.api_prefix)
    app.mount("/exports", StaticFiles(directory=settings.exports_root), name="exports")
    app.mount("/storage", StaticFiles(directory=settings.storage_root), name="storage")

    @app.get("/health", tags=["health"])
    def health_check():  # pragma: no cover - trivial
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8200, reload=True)
