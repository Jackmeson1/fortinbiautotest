import os
import sys
import time
import datetime
import subprocess
from pathlib import Path
import pytest

from src.browser_control import BrowserControl
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService

from src.browser_control import BrowserControl
from src.utils import read_config
import os


@pytest.fixture(scope="session")
def fnbi_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)
    app = FNBIApp(cfg['fnbi']['executable_path'])
    app.start()
    yield app
    app.close()


@pytest.fixture(scope="session")
def fnbi_service():
    service = FNBIService()
    service.start()
    yield service
    service.stop()


@pytest.fixture(scope="function")
def browser():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)
    browser = BrowserControl(
        user_data_dir=cfg['browser']['chrome_user_data_dir'],
        profile_directory=cfg['browser']['chrome_profile_directory']
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session", autouse=True)
def collect_user_logs():
    """Collect user logs at the end of the test session."""
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = artifacts_dir / f"user_logs_{timestamp}.txt"

    yield log_path

    if sys.platform != "win32":
        log_path.write_text("User log collection is only supported on Windows\n")
        return

    try:
        result = subprocess.run(
            ["FNBI", "Collect", "user", "logs"],
            capture_output=True,
            text=True,
            check=False,
        )
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n" + result.stderr)
    except Exception:
        try:
            from pywinauto import Application

            app = Application(backend="uia").connect(title="FortiNBI")
            window = app.window(title="FortiNBI")
            btn = window.child_window(title_re="Collect.*logs")
            btn.click_input()
            time.sleep(5)
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("Logs collected via GUI\n")
        except Exception as exc:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"Failed to collect logs: {exc}\n")
