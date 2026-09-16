import pytest
from app.models.profile import UserProfile
from app.models.schemas import JobSchema
from app.core.matching import MatchEngine

@pytest.fixture
def profile():
    """Provides a standard user profile for all matching tests."""
    return UserProfile(
        required_skills=["Python", "PyTest", "Playwright"], # 2 points each (Max 6)
        optional_skills=["Docker", "Jenkins"],              # 1 point each (Max 2)
        banned_keywords=["Java", "C#"]
    )

@pytest.fixture
def engine(profile):
    """Provides an instantiated MatchEngine."""
    return MatchEngine(profile)

@pytest.mark.unit
def test_perfect_match(engine):
    job = JobSchema(
        title="Senior SDET", company="TechCorp", location="Remote", url="http://x.com", source="API",
        description="Must know Python, Playwright, PyTest, Docker, and Jenkins."
    )
    
    result = engine.score_job(job)
    
    assert result.match_score == 100.0
    assert len(result.matching_skills) == 5
    assert len(result.missing_skills) == 0

@pytest.mark.unit
def test_partial_match_tracks_missing_skills(engine):
    job = JobSchema(
        title="QA Engineer", company="Startup", location="Bengaluru", url="http://y.com", source="API",
        description="Looking for Python and PyTest experience. AWS is a plus."
    )
    
    result = engine.score_job(job)
    
    # Has 2 required (4 pts). Missing 1 required (Playwright) and 2 optional (Docker, Jenkins).
    # Total possible: 8. Actual: 4. Score = 50.0%
    assert result.match_score == 50.0
    assert "Playwright" in result.missing_skills
    assert "Python" in result.matching_skills

@pytest.mark.unit
def test_banned_keyword_drops_score_to_zero(engine):
    job = JobSchema(
        title="Automation", company="Enterprise", location="Remote", url="http://z.com", source="API",
        description="Java is mandatory. We also use Python."
    )
    
    result = engine.score_job(job)
    
    # Despite having "Python", the banned keyword "Java" triggers immediate 0.
    assert result.match_score == 0.0