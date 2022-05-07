from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    engine: str
    user: str
    password: str
    host: str
    port: str
    database: str

    class Config:
        env_prefix = "DB_"
        env_file = ".env"


db_settings = DatabaseSettings()
