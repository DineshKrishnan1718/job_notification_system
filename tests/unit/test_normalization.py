import pytest
from app.core.normalization import normalize_location, normalize_text


@pytest.mark.unit
def test_normalize_text():
    assert normalize_text("  Python   SDET ") == "python sdet"


@pytest.mark.unit
def test_location_aliases():
    assert normalize_location("Bangalore") == "bengaluru"
    assert normalize_location("BLR") == "bengaluru"
    assert normalize_location("WFH") == "remote"
