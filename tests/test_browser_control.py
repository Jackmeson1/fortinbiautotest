import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.browser_control import BrowserControl
from src.utils import read_config
import os
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def browser():
    logger.info("Setting up BrowserControl")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)
    control = BrowserControl(
        user_data_dir=cfg['browser']['chrome_user_data_dir'],
        profile_directory=cfg['browser']['chrome_profile_directory']
    )
    yield control
    logger.info("Tearing down BrowserControl")
    control.close()

def test_google_ca_homepage_loads(browser):
    logger.info("Testing Google CA homepage load")
    browser.navigate_to("https://www.google.ca")
    assert browser.is_page_loaded("Google"), "Google homepage did not load correctly"
    assert browser.is_element_present(By.NAME, "q"), "Search box not found on Google homepage"

def test_search_bar_functionality(browser):
    logger.info("Testing search bar functionality")
    browser.navigate_to("https://www.google.ca")
    search_box = browser.driver.find_element(By.NAME, "q")
    search_box.send_keys("Canada")
    search_box.send_keys(Keys.RETURN)
    assert "Canada" in browser.get_page_title(), "Search results page title does not contain 'Canada'"

def test_navigate_to_nonexistent_page(browser):
    logger.info("Testing navigation to non-existent page")
    with pytest.raises(Exception):
        browser.navigate_to("https://www.thispagedeosnotexist123456789.com")

def test_is_element_present_nonexistent(browser):
    logger.info("Testing is_element_present with non-existent element")
    browser.navigate_to("https://www.google.ca")
    assert not browser.is_element_present(By.ID, "nonexistentelement"), "Non-existent element was found"

def test_get_page_source(browser):
    logger.info("Testing get_page_source")
    browser.navigate_to("https://www.example.com")
    page_source = browser.get_page_source()
    assert page_source is not None, "Page source is None"
    assert "Example Domain" in page_source, "Page source does not contain expected content"

def test_multiple_navigation(browser):
    logger.info("Testing multiple navigation")
    browser.navigate_to("https://www.google.ca")
    assert browser.is_page_loaded("Google"), "Google homepage did not load correctly"
    browser.navigate_to("https://www.example.com")
    assert browser.is_page_loaded("Example Domain"), "Example.com did not load correctly"
    browser.navigate_to("https://www.google.ca")
    assert browser.is_page_loaded("Google"), "Google homepage did not load correctly after multiple navigations"

# 如果您的环境支持不同的浏览器，可以添加以下测试
@pytest.mark.skip(reason="Only run if Firefox is installed")
def test_firefox_initialization():
    logger.info("Testing Firefox initialization")
    firefox_control = BrowserControl(browser_type="firefox")
    firefox_control.navigate_to("https://www.google.ca")
    assert firefox_control.is_page_loaded("Google"), "Google homepage did not load correctly in Firefox"
    firefox_control.close()
