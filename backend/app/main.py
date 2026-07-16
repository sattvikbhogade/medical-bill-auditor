from fastapi import FastAPI

from app.core.events import register_startup_events


def create_app() -> FastAPI:
    app = FastAPI(title="Medical Bill Auditor API")
    register_startup_events(app)

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
