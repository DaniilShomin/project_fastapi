import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Настройки приложения
    APP_NAME: str = "Page Analyzer"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    # Безопасность
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    SESSION_COOKIE_NAME: str = "session"

    # База данных
    DB_URL: str = os.getenv("DATABASE_URL", "sqlite3:///db.sqlite3")
    DB_ECHO: bool = DEBUG  # Логировать SQL-запросы в debug режиме

    # Шаблоны
    TEMPLATES_DIR: str = "page_analyzer/templates"
    AUTO_RELOAD_TEMPLATES: bool = DEBUG

    # Статические файлы
    STATIC_DIR: str = "page_analyzer/static"


settings = Settings()
