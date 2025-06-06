import pytest
from src.fnbi_service import FNBIService

@pytest.fixture
def fnbi_service():
    return FNBIService()

def test_service_status(fnbi_service):
    status = fnbi_service.get_status()
    assert "FortiNBI.rating_service" in status

def test_is_running(fnbi_service):
    assert fnbi_service.is_running() in [True, False]