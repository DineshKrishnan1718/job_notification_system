import time
import schedule
from datetime import datetime
from app.main import run_daily_job_pipeline
from app.config.logging_config import logger

def job_with_retry():
    """
    Wraps our main pipeline in a retry loop.
    If the internet drops or a database locks, it tries again before giving up.
    """
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 300  # 5 minutes

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"--- Starting Scheduled Run (Attempt {attempt}/{MAX_RETRIES}) ---")
            
            # Execute our entire Phase 1-6 pipeline
            run_daily_job_pipeline()
            
            logger.info("Scheduled run completed successfully.")
            break  # Success! Break out of the retry loop.
            
        except Exception as e:
            logger.error(f"Scheduled run failed on attempt {attempt}: {e}")
            if attempt < MAX_RETRIES:
                logger.info(f"Waiting {RETRY_DELAY_SECONDS} seconds before retrying...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                logger.critical("All retry attempts exhausted. Pipeline failed for today.")

def start_scheduler():
    """
    Defines the schedule and keeps the Python process alive.
    """
    # Configure the time you want the daily email (e.g., 08:00 AM)
    # Note: This uses the server's local time zone. 
    target_time = "08:00"
    
    schedule.every().day.at(target_time).do(job_with_retry)
    
    logger.info("==================================================")
    logger.info(f"Scheduler active. Job will run daily at {target_time}.")
    logger.info("Current system time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("Press Ctrl+C to exit.")
    logger.info("==================================================")

    # Infinite loop to keep the script running and checking the time
    try:
        while True:
            # Check if any scheduled tasks are due
            schedule.run_pending()
            
            # Sleep for 60 seconds to prevent maxing out the CPU
            time.sleep(60) 
            
    except KeyboardInterrupt:
        logger.info("Scheduler manually stopped by user.")

if __name__ == "__main__":
    start_scheduler()