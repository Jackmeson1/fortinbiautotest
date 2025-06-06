import pytest
from src.utils import wait_for_port, read_config

def test_extension_capp_communication(browser, fnbi_service, fnbi_app):
    # Ensure FNBI service and app are running
    assert fnbi_service.is_running(), "FNBI service is not running"
    assert fnbi_app.is_running(), "FNBI app is not running"

    config = read_config("config/config.yaml")

    # Navigate to a page that should trigger communication
    browser.navigate_to(config["test"]["allowed_url"])

    # Check if the communication port is open
    assert wait_for_port(5000, timeout=30), "Communication port is not open"


    # Additional sanity check that the page loaded
    assert browser.is_page_loaded("Example Domain")

