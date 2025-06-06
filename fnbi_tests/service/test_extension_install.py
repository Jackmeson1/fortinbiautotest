import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from src.fnbi_service import FNBIService
from src.utils import is_process_running


@pytest.mark.parametrize(
    "browser,process_name",
    [
        ("chrome", "chrome_extension.exe"),
        ("firefox", "firefox_extension.exe"),
    ],
)
def test_extension_installation_trigger(browser, process_name):
    """Service should install the extension when it is missing."""
    service = FNBIService()

    # Ensure extension is not already running
    assert not is_process_running(process_name)

    service.start()
    try:
        WebDriverWait(service, 30, poll_frequency=1).until(
            lambda _: is_process_running(process_name)
        )
        assert is_process_running(process_name), f"{browser} extension was not installed"
    finally:
        service.stop()
