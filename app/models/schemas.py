from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class JobSchema(BaseModel):
    model_config = ConfigDict(extra="ignore")

    # Optional for backward-compatible local fixtures; real adapters should always provide it.
    job_id: str = Field(default="local")
    title: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)
    location: str = "Unknown"
    description: str = ""
    url: Optional[HttpUrl] = None
    source: str = Field(..., min_length=1)
    posted_date: datetime = Field(default_factory=utc_now)
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: str = "INR"
    experience_min: Optional[float] = None
    experience_max: Optional[float] = None
    work_type: str = "unknown"
    employment_type: str = "full-time"
    match_score: float = Field(default=0.0, ge=0, le=100)
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)


class SearchCriteria(BaseModel):
    roles: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
