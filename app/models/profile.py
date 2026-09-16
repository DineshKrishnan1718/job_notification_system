from pydantic import BaseModel, Field, model_validator


class UserProfile(BaseModel):
    required_skills: list[str] = Field(default_factory=lambda: ["Python", "Playwright", "PyTest", "API Testing"])
    optional_skills: list[str] = Field(default_factory=lambda: ["Docker", "Jenkins", "SQL", "Linux", "CI/CD"])
    banned_keywords: list[str] = Field(default_factory=lambda: ["Java", "C#", "Ruby"])
    locations: list[str] = Field(default_factory=lambda: ["Bengaluru", "Remote"])
    min_experience: float = 3
    max_experience: float = 6
    min_salary_lpa: float = 8

    @model_validator(mode="after")
    def validate_experience(self):
        if self.min_experience > self.max_experience:
            raise ValueError("min_experience cannot be greater than max_experience")
        return self
