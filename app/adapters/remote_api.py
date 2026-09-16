import requests
from app.adapters.base import BaseJobSource
from app.models.schemas import JobSchema, SearchCriteria


class PublicJobAPIAdapter(BaseJobSource):
    """Generic JSON adapter for a permitted/public jobs API.

    Set JOB_API_URL to a real endpoint; the example URL is intentionally not used.
    """

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url.rstrip("/")

    @property
    def name(self) -> str:
        return "PublicAPI"

    def fetch_jobs(self, search_config: SearchCriteria | dict) -> list[JobSchema]:
        criteria = search_config if isinstance(search_config, SearchCriteria) else SearchCriteria(
            roles=search_config.get("JOB_ROLES", []), locations=search_config.get("LOCATIONS", [])
        )
        jobs: list[JobSchema] = []
        with requests.Session() as session:
            session.headers.update({"User-Agent": "JobNotificationSystem/1.0"})
            for role in criteria.roles:
                response = session.get(self.base_url, params={"search": role, "limit": 50}, timeout=20)
                response.raise_for_status()
                for item in response.json().get("results", []):
                    jobs.append(JobSchema(
                        job_id=str(item.get("id") or item.get("job_id") or item.get("url") or item.get("title")),
                        title=item.get("title") or "Unknown Title",
                        company=item.get("company_name") or item.get("company") or "Unknown Company",
                        location=item.get("location") or "Remote",
                        description=item.get("description") or "",
                        url=item.get("apply_url") or item.get("url"),
                        source=self.name,
                        posted_date=item.get("posted_at") or item.get("posted_date"),
                        work_type=item.get("work_type") or "unknown",
                    ))
        return jobs
