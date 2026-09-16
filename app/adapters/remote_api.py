import requests
from typing import List
from datetime import datetime
from app.adapters.base import BaseJobSource
from app.models.schemas import JobSchema

class PublicJobAPIAdapter(BaseJobSource):
    """
    Example adapter for a generic public Job API (e.g., RemoteOK or a Company API).
    """
    BASE_URL = "https://example-jobs-api.com/api/v1/jobs"

    def fetch_jobs(self, search_config: dict) -> List[JobSchema]:
        jobs = []
        # We use a session for connection pooling (faster multiple requests)
        with requests.Session() as session:
            session.headers.update({"User-Agent": "JobNotificationBot/1.0"})
            
            for role in search_config.get("JOB_ROLES", []):
                try:
                    self.logger.info(f"Fetching jobs for role: {role}")
                    
                    # API specific query parameters
                    params = {"search": role, "limit": 50}
                    response = session.get(self.BASE_URL, params=params, timeout=10)
                    
                    # Will raise an HTTPError if status code is 4xx or 5xx
                    response.raise_for_status()  
                    
                    data = response.json()
                    
                    # Data Normalization
                    for item in data.get("results", []):
                        job = JobSchema(
                            title=item.get("title", "Unknown Title"),
                            company=item.get("company_name", "Unknown Company"),
                            location=item.get("location", "Remote"),
                            description=item.get("description", ""),
                            url=item.get("apply_url", ""),
                            source="PublicAPI",
                            posted_date=datetime.now() # Ideally parsed from item.get("posted_at")
                        )
                        jobs.append(job)

                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Network error fetching from PublicAPI: {e}")
                except Exception as e:
                    self.logger.error(f"Unexpected error in PublicAPI: {e}")

        self.logger.info(f"PublicAPI adapter found {len(jobs)} jobs.")
        return jobs