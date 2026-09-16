import time
import schedule
from app.main import run_daily_job_pipeline
from app.config.settings import settings
from app.config.logging_config import logger


def job_with_retry():
    for attempt in range(1, 4):
        try:
            logger.info("Scheduled run attempt %d/3", attempt)
            if run_daily_job_pipeline():
                return
        except Exception:
            logger.exception("Scheduled run failed")
        if attempt < 3:
            time.sleep(300)
    logger.error("All scheduled run attempts exhausted")


def start_scheduler():
    schedule.every().day.at(settings.schedule_time).do(job_with_retry)
    logger.info("Scheduler active at %s (%s)", settings.schedule_time, settings.timezone)
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    start_scheduler()
