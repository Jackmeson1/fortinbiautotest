from src.browser_control import BrowserControl
from src.utils import read_config


def test_navigation_works():
    config = read_config("config/config.yaml")
    browser = BrowserControl()
    try:
        browser.navigate_to(config["test"]["allowed_url"])
        assert browser.is_page_loaded("Example Domain")
    finally:
        browser.close()

