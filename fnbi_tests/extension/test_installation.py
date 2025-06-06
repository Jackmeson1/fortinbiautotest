import os

import pytest

from src.utils import check_file_exists, is_process_running, read_config


def test_extension_installation(browser, fnbi_service):
    # Ensure FNBI service is running
    assert fnbi_service.is_running(), "FNBI service is not running"

    config = read_config("config/config.yaml")

    # Navigate to a page that should trigger extension installation
    browser.navigate_to(config["test"]["allowed_url"])

    # Check if the extension process is running
    assert is_process_running(
        "chrome_extension.exe"
    ), "Extension process is not running"

    # Check if extension files are present in the expected location
    extension_dir = os.path.join(
        config["browser"]["chrome_user_data_dir"],
        config["browser"]["chrome_profile_directory"],
        "Extensions",
        "<extension_id>",
    )
    assert check_file_exists(extension_dir), "Extension files are not present"
