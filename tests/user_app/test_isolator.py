import pytest
from src.fnbi_app import FNBIApp


def test_isolator_installed_when_absent(monkeypatch):
    """User app should install isolator if it is missing on start."""
    app = FNBIApp("dummy/path/FortiNBI.exe")

    isolator_installed = {"state": False}

    def fake_is_isolator_running():
        return isolator_installed["state"]

    def fake_install_isolator():
        isolator_installed["state"] = True

    def fake_start():
        if not app.is_isolator_running():
            app.install_isolator()
        # Simulate application start without launching real binary
        app.started = True

    monkeypatch.setattr(app, "is_isolator_running", fake_is_isolator_running)
    # install_isolator is not implemented in FNBIApp, so allow creating it
    monkeypatch.setattr(app, "install_isolator", fake_install_isolator, raising=False)
    monkeypatch.setattr(app, "start", fake_start)

    app.start()

    assert isolator_installed["state"], "Isolator installation was not triggered"
    assert app.is_isolator_running(), "Isolator state was not updated after install"
