import os
import pytest

from src.browser_control import BrowserControl
from src.fnbi_service import FNBIService
from src.utils import is_process_running, check_file_exists, read_config


def test_edge_extension_installation(fnbi_service):
    """Verify the FNBI Edge extension installs correctly."""
    # Ensure the service is running
    fnbi_service.start()
    assert fnbi_service.is_running(), "FNBI service failed to start"

    config = read_config("config/config.yaml")

    # Launch Edge and navigate to an allowed page
    browser = BrowserControl(browser_type="edge")
    browser.navigate_to(config["test"]["allowed_url"])

    # Validate the extension's process exists
    assert is_process_running("msedge_extension.exe"), "Edge extension process is not running"

    # Validate extension files exist in the expected directory
    edge_data_dir = config["browser"]["chrome_user_data_dir"].replace("Google\\Chrome", "Microsoft\\Edge")
    extension_dir = os.path.join(
        edge_data_dir,
        config["browser"]["chrome_profile_directory"],
        "Extensions",
        "<extension_id>",
    )
    assert check_file_exists(extension_dir), "Edge extension files are not present"

    browser.close()
