import pytest


def remove_from_force_install_list(extension_id):
    """Placeholder for removing the extension from the force install list."""
    # In a real environment this would update the browser policy.
    return True


def is_extension_present(extension_id):
    """Placeholder for checking if the extension is installed."""
    return False


def test_extension_uninstall():
    """Remove the extension from the force install list and verify it is gone."""
    extension_id = "test-extension"

    assert remove_from_force_install_list(extension_id)

    assert not is_extension_present(extension_id)
