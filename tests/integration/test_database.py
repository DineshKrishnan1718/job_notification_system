import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.session import Base
from app.database.crud import save_jobs, get_unemailed_jobs, mark_jobs_as_emailed
from app.models.schemas import JobSchema
from app.models.db_models import Job

# --- FIXTURES ---

@pytest.fixture
def test_db():
    """Creates a fresh, temporary RAM database for each test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    yield db  # Provide the session to the test
    db.close() # Clean up after test completes

@pytest.fixture
def sample_jobs():
    """Provides a list of JobSchemas to test database insertions."""
    job_1 = JobSchema(
        title="Python SDET", company="Google", location="Remote", 
        description="Python test", url="http://a.com", source="API"
    )
    job_1.match_score = 90.0

    # job_2 is identical to job_1 (testing duplicates)
    job_2 = JobSchema(
        title="Python SDET", company="Google", location="Remote", 
        description="Different description, same core job", url="http://b.com", source="API"
    )
    job_2.match_score = 90.0

    job_3 = JobSchema(
        title="QA Automation", company="Amazon", location="Bengaluru", 
        description="Low score job", url="http://c.com", source="API"
    )
    job_3.match_score = 40.0 # Below standard threshold

    return [job_1, job_2, job_3]


# --- TESTS ---

@pytest.mark.integration
def test_save_jobs_prevents_duplicates(test_db, sample_jobs):
    """Tests that identical jobs (Title + Company + Location) are not saved twice."""
    
    # Act: Try to save the duplicate list
    new_jobs_count = save_jobs(test_db, sample_jobs)
    
    # Assert: Even though we passed 3 jobs, only 2 should be saved (job_2 is a duplicate of job_1)
    assert new_jobs_count == 2
    
    # Verify in DB
    total_db_jobs = test_db.query(Job).count()
    assert total_db_jobs == 2

@pytest.mark.integration
def test_get_unemailed_jobs_applies_threshold(test_db, sample_jobs):
    """Tests that we only retrieve jobs above the threshold for emailing."""
    
    save_jobs(test_db, sample_jobs)
    
    # Act: Fetch jobs ready for email (Threshold 70)
    pending_jobs = get_unemailed_jobs(test_db, min_score=70.0)
    
    # Assert: Job 3 scored 40.0, so only Job 1 should be returned
    assert len(pending_jobs) == 1
    assert pending_jobs[0].title == "Python SDET"
    assert pending_jobs[0].is_emailed is False

@pytest.mark.integration
def test_mark_jobs_as_emailed(test_db, sample_jobs):
    """Tests the state change of jobs after a successful email dispatch."""
    
    save_jobs(test_db, sample_jobs)
    pending_jobs = get_unemailed_jobs(test_db, min_score=70.0)
    
    # Act: Mark as emailed
    mark_jobs_as_emailed(test_db, pending_jobs)
    
    # Assert: Checking again should yield 0 jobs
    new_pending_jobs = get_unemailed_jobs(test_db, min_score=70.0)
    assert len(new_pending_jobs) == 0