import pytest
from src.fnbi_app import FNBIApp
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def fnbi_app():
    app = FNBIApp(r"C:\Program Files (x86)\Fortinet\FortiNBI\FortiNBI.exe")
    try:
        app.start()
        yield app
    except Exception as e:
        logger.error(f"Error in fixture: {e}")
        if hasattr(app, 'print_window_info'):
            logger.info("Trying to print window info after error:")
            app.print_window_info()
        else:
            logger.error("Unable to print window info: app not initialized")
        raise
    finally:
        try:
            if hasattr(app, 'close'):
                app.close()
        except Exception as e:
            logger.error(f"Error closing app: {e}")

def test_fnbi_app_starts(fnbi_app):
    assert fnbi_app.is_running()
    fnbi_app.print_window_info()

def test_get_status(fnbi_app):
    status = fnbi_app.get_status()
    assert status is not None
    logger.info(f"Status: {status}")

def test_window_visibility(fnbi_app):
    assert fnbi_app.main_window.is_visible(), "Main window is not visible"
    assert fnbi_app.main_window.is_enabled(), "Main window is not enabled"
    logger.info(f"Window title: {fnbi_app.main_window.window_text()}")
    logger.info(f"Window class: {fnbi_app.main_window.class_name()}")

def test_window_structure(fnbi_app):
    fnbi_app.print_window_info()
    assert fnbi_app.main_window.exists(), "Main window does not exist"
