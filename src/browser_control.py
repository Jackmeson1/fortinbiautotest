import time

from selenium import webdriver
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging

logger = logging.getLogger(__name__)

class BrowserControl:
    def __init__(self, browser_type="chrome", user_data_dir=None, profile_directory=None):
        if browser_type == "chrome":
            chrome_options = Options()
            if user_data_dir:
                logger.info(f"Using Chrome user data directory: {user_data_dir}")
                chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            if profile_directory:
                logger.info(f"Using Chrome profile directory: {profile_directory}")
                chrome_options.add_argument(f"profile-directory={profile_directory}")
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                logger.error(f"Failed to initialize Chrome driver: {e}")
                raise
        elif browser_type == "firefox":
            try:
                self.driver = webdriver.Firefox()
            except Exception as e:
                logger.error(f"Failed to initialize Firefox driver: {e}")
                raise
        else:
            raise ValueError("Unsupported browser type")
        logger.info(f"Browser {browser_type} initialized successfully")

    # ... (其余方法保持不变)

    def navigate_to(self, url):
        logger.info(f"Navigating to: {url}")
        try:
            self.driver.get(url)
        except Exception as e:
            logger.warning(f"Exception during navigation: {e}")
            # 可能需要在这里添加一些重试逻辑
            pass

    def is_page_loaded(self, title):
        logger.info(f"Checking if page with title '{title}' is loaded")
        try:
            WebDriverWait(self.driver, 10).until(EC.title_contains(title))
            logger.info("Page loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"Page load check failed: {e}")
            return False

    def is_element_present(self, by, value):
        logger.info(f"Checking for element presence: {by}={value}")
        try:
            self.driver.find_element(by, value)
            logger.info("Element found")
            return True
        except Exception as e:
            logger.warning(f"Element not found: {e}")
            return False

    def close(self):
        logger.info("Closing browser")
        try:
            self.driver.quit()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Failed to close browser: {e}")

    def get_page_title(self):
        try:
            return self.driver.title
        except Exception as e:
            logger.error(f"Failed to get page title: {e}")
            return None

    def get_page_source(self):
        try:
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Failed to get page source: {e}")
            return None

    def wait_for_text_in_page(self, text, timeout=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                page_source = self.driver.page_source
                if text in page_source:
                    return True
            except WebDriverException:
                # 如果发生WebDriverException，我们简单地继续循环
                pass
            time.sleep(0.5)
        return False
