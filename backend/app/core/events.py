from fastapi import FastAPI


def register_startup_events(app: FastAPI) -> None:
    """Register startup hooks for future application initialization."""

    @app.on_event("startup")
    async def startup_event() -> None:
        return None
