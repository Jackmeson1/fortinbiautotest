import pytest
from src.utils import wait_for_port

def test_service_startup(fnbi_service):
    fnbi_service.start()
    assert fnbi_service.is_running(), "FNBI service failed to start"
    assert wait_for_port(5000, timeout=30), "Service port is not open after startup"

def test_service_startup_with_gui_running(fnbi_app, fnbi_service):
    fnbi_app.start()
    fnbi_service.start()
    assert fnbi_service.is_running(), "FNBI service failed to start with GUI running"
    assert fnbi_app.is_running(), "FNBI app stopped running after service start"

def test_service_termination(fnbi_service):
    fnbi_service.start()
    fnbi_service.stop()
    assert not fnbi_service.is_running(), "FNBI service failed to stop"