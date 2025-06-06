_license_active = False


def send_alive_request():
    """Placeholder for sending an alive request to the extension."""
    return {"status": "ok"}


def activate_license():
    global _license_active
    _license_active = True
    return True


def deactivate_license():
    global _license_active
    _license_active = False
    return True


def is_license_active():
    return _license_active


def test_extension_alive():
    """Send an alive request to the extension and verify the response."""
    response = send_alive_request()
    assert response.get("status") == "ok"


def test_license_activation_flow():
    """Activate and deactivate the license using placeholder APIs."""
    assert activate_license()
    assert is_license_active()
    assert deactivate_license()
    assert not is_license_active()
