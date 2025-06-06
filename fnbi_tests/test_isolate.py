import pytest
from selenium import webdriver

import config
from src.browser_control import BrowserControl
from src.fnbi_app import FNBIApp


@pytest.fixture
def fnbi_app():
    return FNBIApp(config.fnbi["app_path"])


@pytest.fixture
def browser():
    driver = webdriver.Chrome(executable_path=config.browsers["chrome"]["driver_path"])
    yield driver
    driver.quit()


def test_isolate_functionality(fnbi_app, browser):
    browser_control = BrowserControl(browser)

    # Navigate to a URL that should be isolated
    browser_control.navigate(config.test_urls["isolate"])

    # Check if WSL2 sandbox browser is opened
    assert browser_control.is_wsl_sandbox_opened(), "WSL2 sandbox browser did not open"

    # Verify isolation (e.g., check for specific elements or behavior in the isolated browser)
    assert browser_control.verify_isolation(), "Page is not properly isolated"


# Add more test cases for isolate functionality
