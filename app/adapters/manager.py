import time
from app.models.schemas import JobSchema, SearchCriteria
from app.adapters.base import BaseJobSource
from app.config.logging_config import logger


class JobSourceManager:
    def __init__(self):
        self.sources: list[BaseJobSource] = []
        self.logger = logger.getChild("JobSourceManager")

    def register_source(self, source: BaseJobSource):
        self.sources.append(source)
        self.logger.info("Registered source adapter: %s", source.name)

    def fetch_all_jobs(self, search_config: SearchCriteria | dict) -> list[JobSchema]:
        criteria = search_config if isinstance(search_config, SearchCriteria) else SearchCriteria(
            roles=search_config.get("JOB_ROLES", []), locations=search_config.get("LOCATIONS", [])
        )
        all_jobs: list[JobSchema] = []
        for source in self.sources:
            started = time.perf_counter()
            try:
                jobs = source.fetch_jobs(criteria)
                all_jobs.extend(jobs)
                self.logger.info("Source %s returned %d jobs in %.2fs", source.name, len(jobs), time.perf_counter() - started)
            except Exception:
                self.logger.exception("Source %s failed", source.name)
        self.logger.info("Total jobs collected: %d", len(all_jobs))
        return all_jobs
