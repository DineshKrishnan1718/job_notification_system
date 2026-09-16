from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


def utc_now():
    return datetime.now(timezone.utc)


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    source = Column(String, nullable=False, index=True)
    source_job_id = Column(String, nullable=False)
    title = Column(String, nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    location = Column(String, index=True)
    description = Column(Text)
    url = Column(String, nullable=True)
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_currency = Column(String, default="INR")
    experience_min = Column(Float)
    experience_max = Column(Float)
    work_type = Column(String, default="unknown")
    employment_type = Column(String, default="full-time")
    match_score = Column(Float, default=0.0)
    matching_skills = Column(Text, default="")
    missing_skills = Column(Text, default="")
    is_emailed = Column(Boolean, default=False, nullable=False, index=True)
    discovered_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    posted_at = Column(DateTime(timezone=True))
    job_hash = Column(String, unique=True, index=True, nullable=False)
    content_hash = Column(String, index=True)
    company = relationship("Company", back_populates="jobs")

    __table_args__ = (Index("ix_jobs_source_source_job_id", "source", "source_job_id", unique=True),)


class JobRun(Base):
    __tablename__ = "job_runs"
    id = Column(Integer, primary_key=True)
    started_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    completed_at = Column(DateTime(timezone=True))
    status = Column(String, nullable=False, default="RUNNING")
    sources_attempted = Column(Integer, default=0)
    sources_succeeded = Column(Integer, default=0)
    sources_failed = Column(Integer, default=0)
    jobs_fetched = Column(Integer, default=0)
    jobs_unique = Column(Integer, default=0)
    jobs_matched = Column(Integer, default=0)
    jobs_notified = Column(Integer, default=0)
    error_message = Column(Text)


class SourceRun(Base):
    __tablename__ = "source_runs"
    id = Column(Integer, primary_key=True)
    job_run_id = Column(Integer, ForeignKey("job_runs.id"), nullable=False, index=True)
    source = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)
    jobs_found = Column(Integer, default=0)
    duration_ms = Column(Integer, default=0)
    error_message = Column(Text)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    recipient = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDING")
    sent_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
