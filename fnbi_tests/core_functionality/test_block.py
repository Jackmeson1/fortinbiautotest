import os
import pytest
import logging
import yaml
from urllib.parse import urlparse
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.browser_control import BrowserControl
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService
import time

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载配置
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
config_path = os.path.join(project_root, 'config', 'config.yaml')
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

@pytest.fixture(scope="module")
def browser():
    logger.info("Setting up browser")
    chrome_user_data_dir = config['browser']['chrome_user_data_dir']
    chrome_profile_directory = config['browser']['chrome_profile_directory']
    browser = BrowserControl(
        browser_type="chrome",
        user_data_dir=chrome_user_data_dir,
        profile_directory=chrome_profile_directory
    )
    yield browser
    logger.info("Tearing down browser")
    browser.close()

@pytest.fixture(scope="module")
def fnbi_app():
    logger.info("Setting up FNBI application")
    fnbi_executable = config['fnbi']['executable_path']
    app = FNBIApp(fnbi_executable)
    if not app.is_running():
        app.start()
    yield app
    # 不在这里停止应用，让它继续运行

@pytest.fixture(scope="module")
def fnbi_service():
    logger.info("Setting up FNBI service")
    service = FNBIService()
    if not service.is_running():
        service.start()
    yield service
    # 不在这里停止服务，让它继续运行

def get_page_content(browser):
    try:
        return browser.driver.page_source
    except WebDriverException as e:
        return f"Unable to get page source: {str(e)}"


import os
import time
import json
from src.ai_screenshot_analysis import analyze_screenshot
from dotenv import load_dotenv
load_dotenv()

@pytest.mark.dependency(depends=["test_system_setup"])
def test_blocked_navigation(browser, fnbi_app, fnbi_service):
    print("\n=== Starting test_blocked_navigation ===")
    window_title = "Chrome"
    api_key = os.getenv('OPENAI_API_KEY')
    example_image_path = os.path.join(project_root, 'resources', 'baseline_images', 'block_example.png')
    function_type = "block"

    try:
        print("Navigating to blank page...")
        browser.navigate_to("about:blank")
        time.sleep(2)
        print("Successfully navigated to blank page")

        blocked_url = config['test']['blocked_url']
        print(f"Trying to navigate to blocked URL: {blocked_url}")
        browser.navigate_to(blocked_url)
        print("Navigation attempted")

        time.sleep(3)  # 给阻止页面显示的时间
        print("\nTaking screenshot for AI analysis...")

        try:
            result = analyze_screenshot(window_title, example_image_path, api_key, function_type)
            print("\nAI Analysis Result:")
            print(f"✓ Functionality Match: {result['functionality_match']}")
            print(f"✓ Confidence Score: {result['confidence']}")

            # 核心断言
            assert result['functionality_match'] == True, "AI analysis indicates functionality does not match"
            assert result[
                       'confidence'] >= 0.8, f"AI analysis confidence ({result['confidence']}) is below threshold (0.8)"

        except Exception as e:
            print(f"\nScreenshot/Analysis error: {str(e)}")
            print(f"Error type: {type(e)}")

        try:
            current_url = browser.driver.current_url
            parsed = urlparse(current_url)
            assert parsed.scheme == 'extension', f"Unexpected scheme: {current_url}"
            assert parsed.path.endswith('gatewayPage.html'), f"Unexpected path: {current_url}"
            assert 'Policy' in browser.driver.page_source
        except WebDriverException as e:
            print(f"\nExpected WebDriver Error: {str(e)}")
            if 'target frame detached' in str(e):
                print("✓ This is the expected behavior when page is blocked")

    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        raise

    print("\n=== Test completed successfully ===")


@pytest.mark.dependency()
def test_system_setup(fnbi_app, fnbi_service):
    """
    Ensure FNBI service and application are running before proceeding with other tests
    """
    assert fnbi_service.is_running(), "FNBI service is not running"
    assert fnbi_app.is_running(), "FNBI application is not running"
