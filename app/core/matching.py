import re
from typing import List, Tuple
from app.models.schemas import JobSchema
from app.models.profile import UserProfile
from app.config.logging_config import logger

class MatchEngine:
    def __init__(self, profile: UserProfile):
        self.profile = profile
        self.logger = logger.getChild("MatchEngine")

    def _extract_skills(self, text: str, skills_to_check: List[str]) -> Tuple[List[str], List[str]]:
        """
        Uses Regex word boundaries to find isolated skills in a block of text.
        Returns: (found_skills, missing_skills)
        """
        found = []
        missing = []
        text_lower = text.lower()

        for skill in skills_to_check:
            # \b ensures we match the whole word. 
            # re.escape safely escapes special characters (like C++ or CI/CD)
            pattern = rf"\b{re.escape(skill.lower())}\b"
            
            if re.search(pattern, text_lower):
                found.append(skill)
            else:
                missing.append(skill)
                
        return found, missing

    def score_job(self, job: JobSchema) -> JobSchema:
        """
        Calculates a percentage score for a job based on the user's profile.
        Updates the job object in-place.
        """
        # 1. Check for banned keywords (Hard Filter)
        banned_found, _ = self._extract_skills(job.description, self.profile.banned_keywords)
        if banned_found:
            self.logger.info(f"Skipping {job.title} - Found banned keywords: {banned_found}")
            job.match_score = 0.0
            return job

        # 2. Extract Required & Optional Skills
        req_found, req_missing = self._extract_skills(job.description, self.profile.required_skills)
        opt_found, opt_missing = self._extract_skills(job.description, self.profile.optional_skills)

        # 3. Apply Weighting System
        # Let's say Required = 2 points, Optional = 1 point
        REQUIRED_WEIGHT = 2
        OPTIONAL_WEIGHT = 1

        max_possible_score = (len(self.profile.required_skills) * REQUIRED_WEIGHT) + \
                             (len(self.profile.optional_skills) * OPTIONAL_WEIGHT)
                             
        if max_possible_score == 0:
            return job # Avoid division by zero if profile is empty

        actual_score = (len(req_found) * REQUIRED_WEIGHT) + (len(opt_found) * OPTIONAL_WEIGHT)

        # 4. Calculate Percentage
        match_percentage = round((actual_score / max_possible_score) * 100, 2)

        # 5. Enrich the Job Data Model
        job.match_score = match_percentage
        job.matching_skills = req_found + opt_found
        job.missing_skills = req_missing + opt_missing
        
        return job