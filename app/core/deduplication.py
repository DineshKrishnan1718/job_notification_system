import hashlib

def generate_job_hash(title: str, company: str, location: str) -> str:
    """Creates a unique deterministic hash for a job."""
    # Convert to lowercase and strip spaces to normalize: "Senior QA" == "senior qa"
    raw_string = f"{title.strip().lower()}|{company.strip().lower()}|{location.strip().lower()}"
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()