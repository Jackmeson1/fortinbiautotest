from src.utils import read_config


def test_navigate_to_allowed_page(browser):
    """Verify that navigation to an allowed URL succeeds."""
    config = read_config("config/config.yaml")
    browser.navigate_to(config["test"]["allowed_url"])
    assert browser.is_page_loaded("Example Domain")
