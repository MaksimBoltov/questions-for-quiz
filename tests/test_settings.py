import os

from dotenv import load_dotenv

from app.settings import DatabaseSettings


def test_database_settings():
    """Testing the correct unloading of data from environment variables."""
    db_settings = DatabaseSettings()
    load_dotenv()
    assert db_settings.engine == os.getenv("DB_ENGINE")
    assert db_settings.user == os.getenv("DB_USER")
    assert db_settings.password == os.getenv("DB_PASSWORD")
    assert db_settings.host == os.getenv("DB_HOST")
    assert db_settings.port == os.getenv("DB_PORT")
    assert db_settings.database == os.getenv("DB_DATABASE")
