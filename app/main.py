from app.config.settings import settings
from app.config.logging_config import logger
from app.adapters.manager import JobSourceManager
from app.adapters.remote_api import PublicJobAPIAdapter
from app.models.profile import UserProfile
from app.models.schemas import SearchCriteria
from app.core.matching import MatchEngine
from app.core.normalization import normalize_job
from app.database.session import SessionLocal
from app.database.crud import (
    save_jobs, get_unemailed_jobs, mark_jobs_as_emailed,
    create_job_run, finish_job_run,
)
from app.notifications.email_sender import EmailService


def build_profile() -> UserProfile:
    return UserProfile(
        required_skills=settings.required_skills,
        optional_skills=settings.preferred_skills,
        banned_keywords=settings.banned_keywords,
        locations=settings.locations,
        min_experience=settings.min_experience,
        max_experience=settings.max_experience,
        min_salary_lpa=settings.min_salary_lpa,
    )


def build_source_manager() -> JobSourceManager:
    manager = JobSourceManager()
    if settings.job_api_url:
        manager.register_source(PublicJobAPIAdapter(settings.job_api_url))
    return manager


def run_daily_job_pipeline() -> bool:
    """Run one complete job-search cycle. Returns True on success."""
    db = SessionLocal()
    run = create_job_run(db)
    try:
        logger.info("Starting job notification run %s", run.id)
        criteria = SearchCriteria(roles=settings.job_roles, locations=settings.locations)
        manager = build_source_manager()
        raw_jobs = manager.fetch_all_jobs(criteria)
        run.jobs_fetched = len(raw_jobs)
        run.sources_attempted = len(manager.sources)

        normalized = [normalize_job(job) for job in raw_jobs]
        engine = MatchEngine(build_profile())
        scored = [engine.score_job(job) for job in normalized]
        run.jobs_matched = sum(job.match_score >= settings.match_threshold for job in scored)

        run.jobs_unique = save_jobs(db, scored)
        pending = get_unemailed_jobs(db, settings.match_threshold)
        if pending:
            EmailService().send_daily_report(pending)
            mark_jobs_as_emailed(db, pending, settings.email_to)
            run.jobs_notified = len(pending)

        finish_job_run(db, run, "SUCCESS")
        logger.info("Job notification run %s completed", run.id)
        return True
    except Exception as exc:
        logger.exception("Job notification run %s failed", run.id)
        finish_job_run(db, run, "FAILED", str(exc))
        return False
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(0 if run_daily_job_pipeline() else 1)
