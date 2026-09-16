import pytest
from app.core.deduplication import generate_job_hash, generate_source_hash


@pytest.mark.unit
def test_job_hash_is_case_and_whitespace_insensitive():
    assert generate_job_hash("Python SDET", "Acme", "Bengaluru") == generate_job_hash(" python sdet ", "ACME", "BENGALURU")


@pytest.mark.unit
def test_source_hash_changes_when_source_id_changes():
    assert generate_source_hash("naukri", "1") != generate_source_hash("naukri", "2")
