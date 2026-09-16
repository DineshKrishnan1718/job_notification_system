import re
import unicodedata
from app.models.schemas import JobSchema


def normalize_text(value: str | None) -> str:
    if not value:
        return ""
    value = unicodedata.normalize("NFKC", value).lower().strip()
    return re.sub(r"\\s+", " ", value)


def normalize_location(value: str | None) -> str:
    text = normalize_text(value)
    aliases = {"bangalore": "bengaluru", "blr": "bengaluru", "wfh": "remote"}
    return aliases.get(text, text)


def normalize_job(job: JobSchema) -> JobSchema:
    job.title = normalize_text(job.title).title()
    job.company = normalize_text(job.company).title()
    job.location = normalize_location(job.location)
    job.description = job.description.strip()
    job.work_type = normalize_text(job.work_type) or "unknown"
    job.source = normalize_text(job.source)
    return job
