import pytest

from src.browser_control import BrowserControl
from src.fnbi_app import FNBIApp
from src.fnbi_service import FNBIService


class TestUserAppServiceCommunication:

    def test_app_reconnect_to_service(self, fnbi_app, fnbi_service):
        """
        Test case 3.1.1: The app can reconnect to the service
        """
        # Start the service (no.1)
        fnbi_service.start()
        assert (
            fnbi_app.is_connected_to_service()
        ), "App failed to connect to service on first start"

        # Stop the service
        fnbi_service.stop()
        assert (
            not fnbi_app.is_connected_to_service()
        ), "App still connected after service stop"

        # Start the service (no.2)
        fnbi_service.start()
        assert (
            fnbi_app.is_connected_to_service()
        ), "App failed to reconnect to service on second start"

    def test_service_port_detection(self, fnbi_app, fnbi_service, port_occupier):
        """
        Test case 3.1.2: User app can detect the service port given a range of ports
        """
        # Start the service
        fnbi_service.start()
        assert (
            fnbi_app.is_connected_to_service()
        ), "App failed to connect to service on first start"

        # Stop the service
        fnbi_service.stop()

        # Occupy the previous port
        previous_port = fnbi_service.get_last_used_port()
        port_occupier.occupy_port(previous_port)

        # Start the service again
        fnbi_service.start()
        assert (
            fnbi_app.is_connected_to_service()
        ), "App failed to connect to service on second start with different port"

    def test_proxy_message_exchange(self, fnbi_app, fnbi_service, config):
        """
        Test case 3.1.3: proxy messages are correctly exchanged
        """
        config.reset_fpx_addr_json()
        config.setup_proxy()

        fnbi_service.start()
        fnbi_app.start()

        assert (
            fnbi_app.get_fpx_addr() == config.get_expected_fpx_addr()
        ), "FPX address not correctly inferred from proxy config"

    def test_isolate_request_isolator_not_running(
        self, fnbi_app, fnbi_service, browser_control
    ):
        """
        Test case 3.1.4: Isolate request is handled when isolator is not running
        """
        fnbi_app.start()
        fnbi_service.start()
        fnbi_app.stop_isolator()

        browser_control.navigate_to_isolated_page()

        assert fnbi_app.is_isolator_running(), "Isolator did not start automatically"
        assert (
            browser_control.is_showing_interception_page()
        ), "Original browser not showing interception page"
        assert (
            browser_control.is_isolated_page_visible()
        ), "Isolated page not visible in browser"

    def test_isolate_request_isolator_running(
        self, fnbi_app, fnbi_service, browser_control
    ):
        """
        Test case 3.1.5: Isolate request is handled when isolator is running
        """
        fnbi_app.start()
        fnbi_service.start()
        fnbi_app.wait_for_isolator_running()

        browser_control.navigate_to_isolated_page()

        assert (
            browser_control.is_request_in_isolated_browser()
        ), "Request not shown in isolated browser"
        assert (
            browser_control.is_showing_interception_page()
        ), "Original browser not showing interception page"


# Add more test methods as needed
