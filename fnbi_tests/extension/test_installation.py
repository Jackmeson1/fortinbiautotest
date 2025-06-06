import pytest
from src.utils import is_process_running, check_file_exists

def test_extension_installation(browser, fnbi_service):
    # Ensure FNBI service is running
    assert fnbi_service.is_running(), "FNBI service is not running"

    # Navigate to a page that should trigger extension installation
    browser.navigate_to("https://example.com")

    # Check if the extension process is running
    assert is_process_running("chrome_extension.exe"), "Extension process is not running"

    # Check if extension files are present in the expected location
    extension_path = r"C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\Extensions\<extension_id>"
    assert check_file_exists(extension_path), "Extension files are not present"

def test_extension_uninstallation(browser, fnbi_service):
    # TODO: Implement test for extension uninstallation
    pass

def test_extension_update(browser, fnbi_service):
    # TODO: Implement test for extension update
    pass
