from sqlalchemy.orm import Session
from typing import List
from app.models.db_models import Job, Company
from app.models.schemas import JobSchema
from app.core.deduplication import generate_job_hash
from app.config.logging_config import logger

def get_or_create_company(db: Session, company_name: str) -> int:
    """Finds a company by name, or creates it if it doesn't exist."""
    company = db.query(Company).filter(Company.name == company_name).first()
    if not company:
        company = Company(name=company_name)
        db.add(company)
        db.commit()
        db.refresh(company)
    return company.id

def save_jobs(db: Session, parsed_jobs: List[JobSchema]) -> int:
    """
    Takes our Pydantic schemas, converts them to SQLAlchemy models, 
    checks for duplicates, and saves the new ones.
    Returns the number of newly inserted jobs.
    """
    new_jobs_count = 0
    
    for schema in parsed_jobs:
        # 1. Generate unique identifier
        job_hash = generate_job_hash(schema.title, schema.company, schema.location)
        
        # 2. Check if job already exists in database
        existing_job = db.query(Job).filter(Job.job_hash == job_hash).first()
        
        if existing_job:
            # We already have this job. Skip it.
            continue
            
        # 3. Handle Company Relation
        company_id = get_or_create_company(db, schema.company)
        
        # 4. Create new Database Record
        new_job = Job(
            title=schema.title,
            company_id=company_id,
            location=schema.location,
            description=schema.description,
            url=str(schema.url),
            source=schema.source,
            match_score=schema.match_score,
            matching_skills=",".join(schema.matching_skills),
            missing_skills=",".join(schema.missing_skills),
            job_hash=job_hash,
            is_emailed=False  # Brand new, hasn't been emailed yet!
        )
        
        db.add(new_job)
        new_jobs_count += 1
        
    # 5. Commit the transaction
    db.commit()
    logger.info(f"Database sync complete. Added {new_jobs_count} new jobs.")
    return new_jobs_count

def get_unemailed_jobs(db: Session, min_score: float = 70.0) -> List[Job]:
    """Retrieves all jobs that haven't been emailed yet, filtered by our threshold."""
    return db.query(Job)\
             .filter(Job.is_emailed == False)\
             .filter(Job.match_score >= min_score)\
             .order_by(Job.match_score.desc())\
             .all()

def mark_jobs_as_emailed(db: Session, jobs: List[Job]):
    """Updates the status of jobs after a successful email dispatch."""
    for job in jobs:
        job.is_emailed = True
    db.commit()