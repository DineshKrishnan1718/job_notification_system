from pydantic import BaseModel
from typing import List

class UserProfile(BaseModel):
    # Mandatory skills (e.g., must have, weight = 2)
    required_skills: List[str] = ["Python", "Playwright", "PyTest", "API Testing"]
    
    # Good to have (e.g., nice to have, weight = 1)
    optional_skills: List[str] = ["Docker", "Jenkins", "SQL", "Linux", "CI/CD"]
    
    # Hard filters (If these don't match, score is automatically 0)
    banned_keywords: List[str] = ["Java", "C#", "Ruby"]