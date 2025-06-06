import pytest
from src.utils import wait_for_port

def test_extension_capp_communication(browser, fnbi_service, fnbi_app):
    # Ensure FNBI service and app are running
    assert fnbi_service.is_running(), "FNBI service is not running"
    assert fnbi_app.is_running(), "FNBI app is not running"

    # Navigate to a page that should trigger communication
    browser.navigate_to("https://example.com")

    # Check if the communication port is open
    assert wait_for_port(5000, timeout=30), "Communication port is not open"

    # TODO: Add more specific checks for communication between extension and CAPP

def test_extension_fpx_communication(browser, fnbi_service):
    # TODO: Implement test for communication between extension and FPX
    pass

def test_extension_service_communication(browser, fnbi_service):
    # TODO: Implement test for communication between extension and FNBI service
    pass
