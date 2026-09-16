from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    job_roles: list[str] = ["QA Automation Engineer", "Python Automation Engineer"]
    locations: list[str] = ["Bengaluru", "Remote"]
    min_experience: float = Field(default=3, ge=0)
    max_experience: float = Field(default=6, ge=0)
    min_salary_lpa: float = Field(default=8, ge=0)
    required_skills: list[str] = ["Python", "Playwright", "PyTest", "API Testing"]
    preferred_skills: list[str] = ["Docker", "Jenkins", "SQL", "Linux", "CI/CD"]
    banned_keywords: list[str] = ["Java", "C#", "Ruby", "Manual Testing"]
    match_threshold: int = Field(default=70, ge=0, le=100)

    database_url: str = "sqlite:///./jobs.db"
    job_api_url: str = ""

    email_host: str = ""
    email_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_to: str = ""
    schedule_time: str = "08:00"
    timezone: str = "Asia/Kolkata"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.min_experience > self.max_experience:
            raise ValueError("MIN_EXPERIENCE cannot be greater than MAX_EXPERIENCE")
        return self


settings = Settings()
