import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")


settings = Settings()
