import os

import pytest
import logging
import yaml
from src.browser_control import BrowserControl
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建到项目根目录的路径
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# 构建配置文件的完整路径
config_path = os.path.join(project_root, 'config', 'config.yaml')
# 加载配置
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

@pytest.fixture(scope="module")
def browser():
    logger.info("Setting up browser")
    chrome_profile_path = config['browser']['chrome_profile_path']
    browser = BrowserControl(profile_path=chrome_profile_path)
    yield browser
    logger.info("Tearing down browser")
    browser.close()

@pytest.fixture(scope="module")
def fnbi_app():
    logger.info("Setting up FNBI application")
    fnbi_executable = config['fnbi']['executable_path']
    app = FNBIApp(fnbi_executable)
    app_was_running = app.is_running()

    if not app_was_running:
        logger.info("Starting FNBI application")
        app.start()
        assert app.is_running(), "FNBI application failed to start"
    else:
        logger.info("FNBI application was already running")

    yield app

    if not app_was_running:
        logger.info("Stopping FNBI application")
        app.close()
        assert not app.is_running(), "FNBI application failed to stop"
    else:
        logger.info("FNBI application was running before the test, leaving it running")

@pytest.fixture(scope="module")
def fnbi_service():
    logger.info("Setting up FNBI service")
    service = FNBIService()
    service_was_running = service.is_running()

    if not service_was_running:
        logger.info("Starting FNBI service")
        service.start()
        assert service.is_running(), "FNBI service failed to start"
    else:
        logger.info("FNBI service was already running")

    yield service

    if not service_was_running:
        logger.info("Stopping FNBI service")
        service.stop()
        assert not service.is_running(), "FNBI service failed to stop"
    else:
        logger.info("FNBI service was running before the test, leaving it running")

@pytest.mark.dependency()
def test_system_setup(fnbi_app, fnbi_service):
    """
    Ensure FNBI service and application are running before proceeding with other tests
    """
    assert fnbi_service.is_running(), "FNBI service is not running"
    assert fnbi_app.is_running(), "FNBI application is not running"

@pytest.mark.dependency(depends=["test_system_setup"])
def test_allowed_navigation(browser, fnbi_app, fnbi_service):
    """
    Test case 1.3.3.1: Allowed navigation
    TEST: with all systems running. Perform ALLOWED navigation
    EXPECTED: Navigation is ALLOWED. Page loads as it would without FNBI
    """
    logger.info("Starting test_allowed_navigation")

    allowed_url = config['test']['allowed_url']
    browser.navigate_to(allowed_url)

    assert browser.is_page_loaded("Example Domain"), "Allowed page did not load correctly"
    assert browser.is_element_present("tag name", "body"), "Page body is missing"
    assert not browser.is_element_present("id", "fnbi-block-page"), "FNBI block page was unexpectedly present"

    logger.info("test_allowed_navigation completed successfully")

@pytest.mark.dependency(depends=["test_system_setup"])
def test_allowed_navigation_after_block(browser, fnbi_app, fnbi_service):
    """
    Test that navigation to an allowed page works after visiting a blocked page
    """
    logger.info("Starting test_allowed_navigation_after_block")

    blocked_url = config['test']['blocked_url']
    browser.navigate_to(blocked_url)
    WebDriverWait(browser.driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    allowed_url = config['test']['allowed_url']
    browser.navigate_to(allowed_url)

    assert browser.is_page_loaded("Example Domain"), "Allowed page did not load correctly after blocked page"
    assert browser.is_element_present("tag name", "body"), "Page body is missing"
    assert not browser.is_element_present("id", "fnbi-block-page"), "FNBI block page was unexpectedly present"

    logger.info("test_allowed_navigation_after_block completed successfully")

# Add more test cases as needed
