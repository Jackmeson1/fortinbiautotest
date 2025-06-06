import pytest

from src.utils import wait_for_port


def test_app_service_connection(fnbi_app, fnbi_service):
    fnbi_service.start()
    fnbi_app.start()

    assert fnbi_app.is_running(), "FNBI app failed to start"
    assert fnbi_service.is_running(), "FNBI service is not running"

    # Check if the app can connect to the service
    assert (
        "Connected" in fnbi_app.get_status()
    ), "FNBI app failed to connect to the service"


def test_app_service_reconnection(fnbi_app, fnbi_service):
    fnbi_service.start()
    fnbi_app.start()

    # Stop the service and restart it
    fnbi_service.stop()
    fnbi_service.start()

    # Check if the app can reconnect to the service
    assert wait_for_port(5000, timeout=30), "Service port did not open after restart"
    assert (
        "Connected" in fnbi_app.get_status()
    ), "FNBI app failed to reconnect to the service"


def test_app_detects_service_port(fnbi_app, fnbi_service):
    # TODO: Implement test for app detecting service port from a range
    pass
