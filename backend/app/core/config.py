from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    app_env: str = getenv("APP_ENV", "development")
    database_url: str = getenv("DATABASE_URL", "")

    def __post_init__(self) -> None:
        if not self.database_url:
            raise RuntimeError("DATABASE_URL environment variable is required")


settings = Settings()
