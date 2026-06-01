from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import api_router
from app.core.config import get_settings

settings = get_settings()

templates = Jinja2Templates(directory=str(settings.storage_root.parent / "app" / "templates"))


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
    app.mount("/static", StaticFiles(directory=str(settings.storage_root.parent / "app" / "static")), name="static")
    app.mount("/exports", StaticFiles(directory=settings.exports_root), name="exports")
    app.mount("/storage", StaticFiles(directory=settings.storage_root), name="storage")

    @app.get("/health", tags=["health"])
    def health_check():  # pragma: no cover - trivial
        return {"status": "ok"}

    @app.get("/", tags=["ui"])
    def page_dashboard(request: Request):
        return templates.TemplateResponse("dashboard.html", {"request": request})

    @app.get("/reports", tags=["ui"])
    def page_reports(request: Request):
        return templates.TemplateResponse("reports.html", {"request": request})

    @app.get("/reports/{report_id}", tags=["ui"])
    def page_report_detail(request: Request, report_id: int):
        return templates.TemplateResponse("report_detail.html", {"request": request, "report_id": report_id})

    @app.get("/photos", tags=["ui"])
    def page_photos(request: Request):
        return templates.TemplateResponse("photos.html", {"request": request})

    @app.get("/tasks", tags=["ui"])
    def page_tasks(request: Request):
        return templates.TemplateResponse("tasks.html", {"request": request})

    @app.get("/signatures", tags=["ui"])
    def page_signatures(request: Request):
        return templates.TemplateResponse("signatures.html", {"request": request})

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8200, reload=True)
