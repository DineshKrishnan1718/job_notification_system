import re
from app.models.schemas import JobSchema
from app.models.profile import UserProfile


class MatchEngine:
    """Deterministic and explainable 0-100 job matching engine."""

    def __init__(self, profile: UserProfile):
        self.profile = profile

    @staticmethod
    def _contains(text: str, term: str) -> bool:
        pattern = rf"(?<!\\w){re.escape(term.lower())}(?!\\w)"
        return re.search(pattern, text.lower()) is not None

    def _skills(self, text: str, skills: list[str]) -> tuple[list[str], list[str]]:
        found, missing = [], []
        for skill in skills:
            (found if self._contains(text, skill) else missing).append(skill)
        return found, missing

    def score_job(self, job: JobSchema) -> JobSchema:
        text = f"{job.title} {job.description}"
        banned = [x for x in self.profile.banned_keywords if self._contains(text, x)]
        if banned:
            job.match_score = 0.0
            job.matching_skills = []
            job.missing_skills = self.profile.required_skills + self.profile.optional_skills
            return job

        req_found, req_missing = self._skills(text, self.profile.required_skills)
        opt_found, opt_missing = self._skills(text, self.profile.optional_skills)
        required_score = (len(req_found) / len(self.profile.required_skills) * 60) if self.profile.required_skills else 60
        optional_score = (len(opt_found) / len(self.profile.optional_skills) * 20) if self.profile.optional_skills else 20
        location_score = 20 if not self.profile.locations or any(self._contains(job.location, x) for x in self.profile.locations) else 0
        job.match_score = round(min(100.0, required_score + optional_score + location_score), 2)
        job.matching_skills = req_found + opt_found
        job.missing_skills = req_missing + opt_missing
        return job
