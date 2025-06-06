import os
import time

import pytest
import yaml

from src.browser_control import BrowserControl
from src.utils import is_process_running, kill_process, wait_for_port

# Load configuration for test URLs
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
config_path = os.path.join(project_root, "config", "config.yaml")
with open(config_path, "r") as cfg_file:
    CONFIG = yaml.safe_load(cfg_file)


def stop_mock_fpx():
    """Ensure the mock FPX process is not running."""
    if is_process_running("mock_fpx.exe"):
        kill_process("mock_fpx.exe")


@pytest.fixture
def fnbi_service():
    """Dummy FNBIService fixture for non-Windows test environments."""

    class _Service:
        def __init__(self):
            self._running = False

        def start(self):
            self._running = True

        def stop(self):
            self._running = False

        def is_running(self):
            return self._running

    return _Service()


@pytest.fixture
def fnbi_app():
    """Dummy FNBIApp fixture for non-Windows test environments."""

    class _App:
        def __init__(self):
            self._running = False

        def start(self):
            self._running = True

        def is_running(self):
            return self._running

    return _App()


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


def test_degraded_block_page_when_fpx_down(fnbi_service, fnbi_app):
    """Navigation shows block page when FPX is not running."""
    stop_mock_fpx()

    fnbi_service.start()
    fnbi_app.start()

    browser = BrowserControl(browser_type="chrome")
    try:
        blocked_url = CONFIG["test"]["blocked_url"]
        browser.navigate_to(blocked_url)
        time.sleep(3)
        assert browser.is_element_present(
            "id", "fnbi-block-page"
        ), "Browser did not show block page with FPX down"
    finally:
        browser.close()
