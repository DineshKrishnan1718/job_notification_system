from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    # Relationship back to jobs
    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    location = Column(String)
    description = Column(Text)
    url = Column(String, nullable=False)
    source = Column(String)  # e.g., LinkedIn, Naukri
    
    # Matching details
    match_score = Column(Float, default=0.0)
    matching_skills = Column(String)  # Stored as comma-separated string for simplicity
    missing_skills = Column(String)
    
    # State tracking
    is_emailed = Column(Boolean, default=False)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    
    # A unique hash to prevent duplicates (Title + Company + Location)
    job_hash = Column(String, unique=True, index=True, nullable=False)

    # Relationship
    company = relationship("Company", back_populates="jobs")