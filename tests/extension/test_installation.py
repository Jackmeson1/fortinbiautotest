import os

from src.utils import read_config


def test_config_contains_browser_paths():
    config = read_config("config/config.yaml")
    assert os.path.isabs(config["browser"]["chrome_user_data_dir"])
    assert config["browser"]["chrome_profile_directory"]
