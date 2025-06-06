import os
import sys
import subprocess
from unittest import mock


def windows_install(installer_path: str, install_dir: str, version: str):
    """Simulate running the Windows installer and writing registry entries."""
    # Run installer silently
    subprocess.run([installer_path, "/quiet"], check=True)

    # Create installation directory and write version file
    os.makedirs(install_dir, exist_ok=True)
    with open(os.path.join(install_dir, "version.txt"), "w") as fp:
        fp.write(version)

    # Update registry with installed version
    import winreg  # noqa: WPS433 - imported dynamically for mocking

    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\FortiNBI")
    try:
        old_version, _ = winreg.QueryValueEx(key, "Version")
    except FileNotFoundError:
        old_version = None

    winreg.SetValueEx(key, "Version", 0, winreg.REG_SZ, version)
    return old_version


@mock.patch("subprocess.run")
@mock.patch("os.makedirs")
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_fresh_installation(mock_open, mock_makedirs, mock_run, tmp_path):
    """Fresh installation on a clean system."""
    mock_winreg = mock.MagicMock()
    mock_winreg.HKEY_LOCAL_MACHINE = mock.sentinel.hklm
    mock_winreg.REG_SZ = mock.sentinel.reg_sz
    mock_winreg.CreateKey.return_value = mock.sentinel.key
    mock_winreg.QueryValueEx.side_effect = FileNotFoundError

    installer = tmp_path / "FortiNBISetup.exe"
    install_dir = tmp_path / "FortiNBI"

    with mock.patch.dict(sys.modules, {"winreg": mock_winreg}):
        old_version = windows_install(str(installer), str(install_dir), "1.0.0")

    assert old_version is None
    mock_run.assert_called_once_with([str(installer), "/quiet"], check=True)
    mock_makedirs.assert_called_once_with(str(install_dir), exist_ok=True)
    mock_open.assert_called_once_with(os.path.join(str(install_dir), "version.txt"), "w")
    mock_winreg.CreateKey.assert_called_once_with(mock_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\FortiNBI")
    mock_winreg.SetValueEx.assert_called_once_with(mock.sentinel.key, "Version", 0, mock_winreg.REG_SZ, "1.0.0")


@mock.patch("subprocess.run")
@mock.patch("os.makedirs")
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_reinstallation_over_existing_setup(mock_open, mock_makedirs, mock_run, tmp_path):
    """Reinstallation over an existing setup."""
    mock_winreg = mock.MagicMock()
    mock_winreg.HKEY_LOCAL_MACHINE = mock.sentinel.hklm
    mock_winreg.REG_SZ = mock.sentinel.reg_sz
    mock_winreg.CreateKey.return_value = mock.sentinel.key
    mock_winreg.QueryValueEx.return_value = ("1.0.0", mock_winreg.REG_SZ)

    installer = tmp_path / "FortiNBISetup.exe"
    install_dir = tmp_path / "FortiNBI"

    with mock.patch.dict(sys.modules, {"winreg": mock_winreg}):
        old_version = windows_install(str(installer), str(install_dir), "1.0.0")

    assert old_version == "1.0.0"
    mock_run.assert_called_once_with([str(installer), "/quiet"], check=True)
    mock_makedirs.assert_called_once_with(str(install_dir), exist_ok=True)
    mock_open.assert_called_once_with(os.path.join(str(install_dir), "version.txt"), "w")
    mock_winreg.SetValueEx.assert_called_once_with(mock.sentinel.key, "Version", 0, mock_winreg.REG_SZ, "1.0.0")


@mock.patch("subprocess.run")
@mock.patch("os.makedirs")
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_direct_upgrade_from_older_version(mock_open, mock_makedirs, mock_run, tmp_path):
    """Direct upgrade from an older version."""
    mock_winreg = mock.MagicMock()
    mock_winreg.HKEY_LOCAL_MACHINE = mock.sentinel.hklm
    mock_winreg.REG_SZ = mock.sentinel.reg_sz
    mock_winreg.CreateKey.return_value = mock.sentinel.key
    mock_winreg.QueryValueEx.return_value = ("0.9.0", mock_winreg.REG_SZ)

    installer = tmp_path / "FortiNBISetup.exe"
    install_dir = tmp_path / "FortiNBI"

    with mock.patch.dict(sys.modules, {"winreg": mock_winreg}):
        old_version = windows_install(str(installer), str(install_dir), "1.0.0")

    assert old_version == "0.9.0"
    mock_run.assert_called_once_with([str(installer), "/quiet"], check=True)
    mock_makedirs.assert_called_once_with(str(install_dir), exist_ok=True)
    mock_open.assert_called_once_with(os.path.join(str(install_dir), "version.txt"), "w")
    mock_winreg.SetValueEx.assert_called_once_with(mock.sentinel.key, "Version", 0, mock_winreg.REG_SZ, "1.0.0")
