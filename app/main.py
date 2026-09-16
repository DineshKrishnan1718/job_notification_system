import sys
from app.config.settings import settings
from app.config.logging_config import logger

# Phase 3: Adapters
from app.adapters.manager import JobSourceManager
from app.adapters.remote_api import PublicJobAPIAdapter

# Phase 4: Matching
from app.models.profile import UserProfile
from app.core.matching import MatchEngine

# Phase 5: Database
from app.database.session import SessionLocal, Base, engine
from app.database.crud import save_jobs, get_unemailed_jobs, mark_jobs_as_emailed

# Phase 6: Notifications
from app.notifications.email_sender import EmailService


def run_daily_job_pipeline():
    logger.info("==================================================")
    logger.info("Starting Daily Job Notification Pipeline...")
    logger.info("==================================================")

    # 0. Database Initialization (Creates tables if they don't exist)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # PHASE 3 & 4 SETUP: Search Config & User Profile
        # ---------------------------------------------------------
        search_config = {
            "JOB_ROLES": settings.JOB_ROLES,
            "LOCATIONS": settings.LOCATIONS
        }

        # In a real app, you might load this from a JSON file or the DB.
        # For now, we define our target resume skills here.
        my_profile = UserProfile(
            required_skills=["Python", "Playwright", "PyTest", "API", "Automation"],
            optional_skills=["Docker", "Jenkins", "SQL", "Linux", "CI/CD", "AWS"],
            banned_keywords=["Java", "C#", "Ruby", "Manual Testing"]
        )
        
        match_engine = MatchEngine(profile=my_profile)

        # ---------------------------------------------------------
        # PHASE 3: Fetch Raw Jobs via Source Adapters
        # ---------------------------------------------------------
        manager = JobSourceManager()
        
        # Register all active sources
        manager.register_source(PublicJobAPIAdapter())
        # manager.register_source(LinkedInAdapter()) # Plug in more later!

        logger.info("Fetching raw jobs from all registered sources...")
        raw_jobs = manager.fetch_all_jobs(search_config)
        
        if not raw_jobs:
            logger.info("No jobs found from any source today. Exiting pipeline.")
            return

        # ---------------------------------------------------------
        # PHASE 4: Score and Filter Jobs
        # ---------------------------------------------------------
        logger.info("Running Match Engine against found jobs...")
        scored_jobs = []
        for job in raw_jobs:
            scored_job = match_engine.score_job(job)
            scored_jobs.append(scored_job)
            
        # ---------------------------------------------------------
        # PHASE 5: Save to Database (Deduplication)
        # ---------------------------------------------------------
        logger.info("Saving jobs to database and checking for duplicates...")
        new_jobs_added = save_jobs(db, scored_jobs)
        logger.info(f"Pipeline identified {new_jobs_added} genuinely new jobs.")

        # ---------------------------------------------------------
        # PHASE 6: Generate Report & Send Email
        # ---------------------------------------------------------
        logger.info(f"Querying DB for unemailed jobs with score >= {settings.MATCH_THRESHOLD}%")
        pending_jobs = get_unemailed_jobs(db, min_score=settings.MATCH_THRESHOLD)

        if pending_jobs:
            logger.info(f"Preparing to email {len(pending_jobs)} high-matching jobs.")
            email_service = EmailService()
            
            try:
                email_service.send_daily_report(pending_jobs)
                
                # VERY IMPORTANT: Only mark as emailed if the email actually succeeded!
                mark_jobs_as_emailed(db, pending_jobs)
                logger.info("Successfully marked jobs as emailed in the database.")
                
            except Exception as e:
                logger.error(f"Email dispatch failed: {e}. Jobs will remain in queue for tomorrow.")
        else:
            logger.info("No new jobs met the match threshold today. No email sent.")

    except Exception as e:
        logger.critical(f"CRITICAL ERROR in main pipeline: {e}", exc_info=True)
        sys.exit(1)
        
    finally:
        # Ensure database connection is closed regardless of success or failure
        db.close()
        logger.info("Database session closed. Pipeline finished.")
        logger.info("==================================================")


if __name__ == "__main__":
    run_daily_job_pipeline()