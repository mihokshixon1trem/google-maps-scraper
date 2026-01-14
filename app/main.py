from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.session import init_db

from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.businesses import router as businesses_router
from app.api.routes.reviews import router as reviews_router
from app.api.routes.exports import router as exports_router


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title=settings.app_name)

    @app.on_event("startup")
    def _startup():
        init_db()

    app.include_router(health_router)
    app.include_router(jobs_router)
    app.include_router(businesses_router)
    app.include_router(reviews_router)
    app.include_router(exports_router)

    return app


app = create_app()
