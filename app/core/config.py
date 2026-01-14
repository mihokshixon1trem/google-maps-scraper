from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "google-maps-business-data-extractor-api"
    api_key: str = "change-me"
    timezone: str = "Asia/Karachi"

    google_api_key: str = ""
    places_base_url: str = "https://maps.googleapis.com/maps/api/place"
    places_language: str = "en"

    default_max_results: int = 60
    default_concurrency: int = 5
    default_requests_per_second: int = 6
    default_max_pages: int = 3

    postgres_host: str = "db"
    postgres_port: int = 5432
    postgres_db: str = "maps_scraper"
    postgres_user: str = "maps"
    postgres_password: str = "maps"

    redis_host: str = "redis"
    redis_port: int = 6379

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
