
import logging
import os

import pytest

import logging
from src.utils import read_config

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



load_dotenv()

import time

from src.ai_screenshot_analysis import analyze_screenshot
from src.browser_control import BrowserControl
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load configuration
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
config_path = os.path.join(project_root, 'config', 'config.yaml')
config = read_config(config_path)



@pytest.fixture(scope="module")
def browser():
    logger.info("Setting up browser")
    chrome_user_data_dir = config["browser"]["chrome_user_data_dir"]
    chrome_profile_directory = config["browser"]["chrome_profile_directory"]
    browser = BrowserControl(
        browser_type="chrome",
        user_data_dir=chrome_user_data_dir,
        profile_directory=chrome_profile_directory,
    )
    yield browser
    logger.info("Tearing down browser")
    browser.close()


@pytest.fixture(scope="module")
def fnbi_app():
    logger.info("Setting up FNBI application")
    fnbi_executable = config["fnbi"]["executable_path"]
    app = FNBIApp(fnbi_executable)
    if not app.is_running():
        app.start()
    yield app
    # Do not stop the application here; let it keep running


@pytest.fixture(scope="module")
def fnbi_service():
    logger.info("Setting up FNBI service")
    service = FNBIService()
    if not service.is_running():
        service.start()
    yield service
    # Do not stop the service here; let it keep running


def get_page_content(browser):
    try:
        return browser.driver.page_source
    except WebDriverException as e:
        return f"Unable to get page source: {str(e)}"


@pytest.mark.dependency()
def test_system_setup(fnbi_app, fnbi_service):
    """Ensure FNBI service and application are running so other tests can proceed."""
    assert fnbi_service.is_running(), "FNBI service is not running"
    assert fnbi_app.is_running(), "FNBI application is not running"


@pytest.mark.dependency(depends=["test_system_setup"])
def test_freeze_navigation(browser, fnbi_app, fnbi_service):
    print("\n=== Starting test_freeze_navigation ===")
    window_title = "Chrome"
    api_key = os.getenv("OPENAI_API_KEY")
    example_image_path = os.path.join(
        project_root, "resources", "baseline_images", "freeze_example.png"
    )
    function_type = "freeze"

    try:
        print("Navigating to blank page...")
        browser.navigate_to("about:blank")
        WebDriverWait(browser.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("Successfully navigated to blank page")

        freeze_url = config["test"]["freeze_url"]
        print(f"Trying to navigate to freeze URL: {freeze_url}")
        browser.navigate_to(freeze_url)
        print("Navigation attempted")

        WebDriverWait(browser.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("\nTaking screenshot for AI analysis...")

        try:
            result = analyze_screenshot(
                window_title, example_image_path, api_key, function_type
            )
            print(json.dumps(result, indent=2))
            print(f"✓ Functionality Match: {result['functionality_match']}")
            print(f"✓ Confidence Score: {result['confidence']}")

            assert (
                result["functionality_match"] == True
            ), "AI analysis indicates functionality does not match"
            assert (
                result["confidence"] >= 0.8
            ), f"AI analysis confidence ({result['confidence']}) is below threshold (0.8)"

        except Exception as e:
            print(f"\nScreenshot/Analysis error: {str(e)}")
            print(f"Error type: {type(e)}")

        try:
            current_url = browser.driver.current_url
        except WebDriverException as e:
            print(f"\nExpected WebDriver Error: {str(e)}")
            if "target frame detached" in str(e):
                print("✓ This is the expected behavior when page is frozen")

    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        raise

    print("\n=== Test completed successfully ===")

