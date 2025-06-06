import pytest
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService
from src.browser_control import BrowserControl

@pytest.fixture(scope="session")
def fnbi_app():
    app = FNBIApp(r"C:\Program Files (x86)\Fortinet\FortiNBI\FortiNBI.exe")
    app.start()
    yield app
    app.close()

@pytest.fixture(scope="session")
def fnbi_service():
    service = FNBIService()
    service.start()
    yield service
    service.stop()

@pytest.fixture(scope="function")
def browser():
    browser = BrowserControl()
    yield browser
    browser.close()
