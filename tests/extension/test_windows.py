
import pytest
import sys
from src.utils import read_config


@pytest.mark.skipif(sys.platform != "win32", reason="Windows specific test")
def test_executable_path_points_to_windows_binary():
    config = read_config("config/config.yaml")
    assert config["fnbi"]["executable_path"].endswith("FortiNBI.exe")


