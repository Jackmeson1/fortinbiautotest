import sys
import time
import pytest
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService

# Skip these tests on non-Windows platforms since pywinauto and the FNBI
# application only run on Windows.
pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows specific test")


class TestGUIServiceControls:
    """Verify service control buttons and status labels in the user GUI."""

    def _get_start_button(self, app: FNBIApp):
        return app.main_window.child_window(title="Start")

    def _get_restart_button(self, app: FNBIApp):
        return app.main_window.child_window(title="Restart")

    def _get_status_label(self, app: FNBIApp):
        return app.main_window.child_window(auto_id="ServiceStateLabel")

    def test_buttons_when_service_stopped(self, fnbi_app: FNBIApp, fnbi_service: FNBIService):
        """Start should be enabled and Restart disabled when the service is stopped."""
        fnbi_service.stop()
        fnbi_app.find_main_window()

        start_btn = self._get_start_button(fnbi_app)
        restart_btn = self._get_restart_button(fnbi_app)

        assert start_btn.is_visible()
        assert start_btn.is_enabled()
        assert not restart_btn.is_enabled()

    def test_buttons_when_service_running(self, fnbi_app: FNBIApp, fnbi_service: FNBIService):
        """Restart should be enabled and Start disabled when the service is running."""
        fnbi_service.start()
        fnbi_app.find_main_window()

        start_btn = self._get_start_button(fnbi_app)
        restart_btn = self._get_restart_button(fnbi_app)

        assert restart_btn.is_visible()
        assert restart_btn.is_enabled()
        assert not start_btn.is_enabled()

    def test_service_state_labels(self, fnbi_app: FNBIApp, fnbi_service: FNBIService):
        """Labels should update to 'Stopped', 'Starting' and 'Running' as the service changes state."""
        fnbi_service.stop()
        fnbi_app.find_main_window()
        label = self._get_status_label(fnbi_app)
        assert "Stopped" in label.window_text()

        fnbi_service.start()
        fnbi_app.find_main_window()
        label = self._get_status_label(fnbi_app)
        assert any(word in label.window_text() for word in ["Starting", "Running"])

        # Wait a bit for the service to reach the running state
        for _ in range(10):
            if fnbi_service.is_running():
                break
            time.sleep(1)
        fnbi_app.find_main_window()
        label = self._get_status_label(fnbi_app)
        assert "Running" in label.window_text()
