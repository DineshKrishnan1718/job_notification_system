from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Search Configuration
    JOB_ROLES: List[str] = ["QA Automation Engineer", "Python Automation Engineer"]
    LOCATIONS: List[str] = ["Bengaluru", "Remote"]
    MIN_EXPERIENCE: int = 3
    MAX_EXPERIENCE: int = 6
    MIN_SALARY_LPA: int = 8
    REQUIRED_SKILLS: List[str] = ["Python", "Playwright", "PyTest", "API Testing"]
    MATCH_THRESHOLD: int = 70  # Minimum score to send an email

    # Database
    DATABASE_URL: str = "sqlite:///./jobs.db"  # Default to local SQLite

    # Email Settings (to be used later)
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_TO: str = ""

    # This tells Pydantic to read from a .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate the settings object to be imported across the app
settings = Settings()