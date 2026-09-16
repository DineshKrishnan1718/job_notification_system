from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class Job(BaseModel):
    """Normalized Job Model used across the entire application."""
    
    job_id: str = Field(..., description="Unique ID from the source platform")
    title: str = Field(..., description="Job Title")
    company_name: str
    location: str
    
    # Optional fields (since platforms might not provide them)
    description: str = "Not Available"
    url: Optional[HttpUrl] = None
    salary_range: str = "Not Available"
    experience_required: str = "Not Available"
    work_type: str = "Not Available" # Remote, Hybrid, On-site
    employment_type: str = "Full-time"
    
    # Metadata
    source: str = Field(..., description="E.g., LinkedIn, Naukri")
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Matched metrics (populated later by the matching engine)
    match_score: float = 0.0
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)

    @property
    def composite_id(self) -> str:
        """
        Creates a unique hash for duplicate detection across platforms.
        Example: QA Automation Engineer-Google-Bengaluru
        """
        clean_title = self.title.strip().lower()
        clean_company = self.company_name.strip().lower()
        clean_location = self.location.strip().lower()
        return f"{clean_title}-{clean_company}-{clean_location}"