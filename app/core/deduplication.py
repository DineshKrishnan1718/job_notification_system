import hashlib
import re


def normalize_key(value: str | None) -> str:
    value = (value or "").strip().lower()
    return re.sub(r"\\s+", " ", value)


def generate_job_hash(title: str, company: str, location: str) -> str:
    raw = "|".join(map(normalize_key, (title, company, location)))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def generate_source_hash(source: str, source_job_id: str) -> str:
    raw = f"{normalize_key(source)}|{normalize_key(source_job_id)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
