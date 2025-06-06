import subprocess
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait

import pytest

from src.utils import is_process_running


@pytest.mark.skipif(sys.platform != "win32", reason="Windows specific test")
def test_notepad_can_launch():
    """Ensure basic Windows apps can run while the extension is installed."""
    proc = subprocess.Popen(["notepad.exe"])
    try:
        WebDriverWait(proc, 5).until(
            lambda _: is_process_running("notepad.exe")
        )
        assert is_process_running("notepad.exe")
    finally:
        proc.terminate()
