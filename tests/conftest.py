import pytest
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService
from src.browser_control import BrowserControl
from src.utils import read_config
import os

@pytest.fixture(scope="session")
def fnbi_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)
    app = FNBIApp(cfg['fnbi']['executable_path'])
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)
    browser = BrowserControl(
        user_data_dir=cfg['browser']['chrome_user_data_dir'],
        profile_directory=cfg['browser']['chrome_profile_directory']
    )
    yield browser
    browser.close()
