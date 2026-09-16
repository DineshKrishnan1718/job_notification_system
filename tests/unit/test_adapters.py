import pytest
from unittest.mock import patch, Mock
from app.adapters.remote_api import PublicJobAPIAdapter

@pytest.mark.unit
@patch("app.adapters.remote_api.requests.Session.get")
def test_public_api_adapter_success(mock_get):
    # 1. Arrange (Set up the mock)
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {
                "title": "Python SDET",
                "company_name": "MockCorp",
                "location": "Remote",
                "description": "Needs PyTest",
                "apply_url": "http://example.com/apply"
            }
        ]
    }
    mock_get.return_value = mock_response

    # 2. Act (Run our adapter)
    adapter = PublicJobAPIAdapter()
    search_config = {"JOB_ROLES": ["SDET"]}
    jobs = adapter.fetch_jobs(search_config)

    # 3. Assert (Verify the behavior)
    assert len(jobs) == 1
    assert jobs[0].title == "Python SDET"
    assert jobs[0].company == "MockCorp"
    assert jobs[0].source == "PublicAPI"
    mock_get.assert_called_once() # Ensures our code actually called requests.get