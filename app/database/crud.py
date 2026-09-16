from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.db_models import Job, Company, JobRun, SourceRun, Notification
from app.models.schemas import JobSchema
from app.core.deduplication import generate_job_hash


def get_or_create_company(db: Session, company_name: str) -> Company:
    company = db.query(Company).filter(Company.name == company_name).first()
    if company:
        return company
    company = Company(name=company_name)
    db.add(company)
    db.flush()
    return company


def save_jobs(db: Session, parsed_jobs: list[JobSchema]) -> int:
    new_count = 0
    for schema in parsed_jobs:
        job_hash = generate_job_hash(schema.title, schema.company, schema.location)
        existing = db.query(Job).filter(Job.job_hash == job_hash).first()
        if existing:
            continue
        company = get_or_create_company(db, schema.company)
        db.add(Job(
            source=schema.source,
            source_job_id=schema.job_id,
            title=schema.title,
            company_id=company.id,
            location=schema.location,
            description=schema.description,
            url=str(schema.url) if schema.url else None,
            salary_min=schema.salary_min,
            salary_max=schema.salary_max,
            salary_currency=schema.salary_currency,
            experience_min=schema.experience_min,
            experience_max=schema.experience_max,
            work_type=schema.work_type,
            employment_type=schema.employment_type,
            match_score=schema.match_score,
            matching_skills=",".join(schema.matching_skills),
            missing_skills=",".join(schema.missing_skills),
            job_hash=job_hash,
            posted_at=schema.posted_date,
            is_emailed=False,
        ))
        new_count += 1
    db.commit()
    return new_count


def get_unemailed_jobs(db: Session, min_score: float = 70.0) -> list[Job]:
    return (db.query(Job)
            .filter(Job.is_emailed.is_(False), Job.match_score >= min_score)
            .order_by(Job.match_score.desc())
            .all())


def mark_jobs_as_emailed(db: Session, jobs: list[Job], recipient: str | None = None):
    for job in jobs:
        job.is_emailed = True
        if recipient:
            db.add(Notification(job_id=job.id, recipient=recipient, status="SENT", sent_at=datetime.now(timezone.utc)))
    db.commit()


def create_job_run(db: Session) -> JobRun:
    run = JobRun(status="RUNNING")
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def finish_job_run(db: Session, run: JobRun, status: str, error_message: str | None = None):
    run.status = status
    run.completed_at = datetime.now(timezone.utc)
    run.error_message = error_message
    db.commit()


def record_source_run(db: Session, job_run_id: int, source: str, status: str, jobs_found: int, duration_ms: int, error_message: str | None = None):
    db.add(SourceRun(job_run_id=job_run_id, source=source, status=status, jobs_found=jobs_found, duration_ms=duration_ms, error_message=error_message))
    db.commit()
