from typing import List
from app.models.schemas import JobSchema
from app.adapters.base import BaseJobSource
from app.config.logging_config import logger

class JobSourceManager:
    def __init__(self):
        self.sources: List[BaseJobSource] = []
        self.logger = logger.getChild("JobSourceManager")

    def register_source(self, source: BaseJobSource):
        """Add an adapter to the manager."""
        self.sources.append(source)
        self.logger.info(f"Registered source adapter: {source.__class__.__name__}")

    def fetch_all_jobs(self, search_config: dict) -> List[JobSchema]:
        """
        Iterates through all registered sources, collects jobs, and handles adapter failures.
        """
        all_jobs = []
        
        for source in self.sources:
            try:
                self.logger.info(f"Starting execution for {source.__class__.__name__}")
                
                # The adapter does its work (API call, Playwright, etc.)
                jobs = source.fetch_jobs(search_config)
                all_jobs.extend(jobs)
                
                self.logger.info(f"Successfully collected {len(jobs)} jobs from {source.__class__.__name__}")
                
            except Exception as e:
                # If an adapter fails entirely, we log the error and CONTINUE to the next source
                self.logger.error(f"CRITICAL FAILURE in {source.__class__.__name__}: {e}")
                continue

        self.logger.info(f"Total jobs collected across all platforms: {all_jobs}")
        return all_jobs