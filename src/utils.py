import ctypes
import logging
import os
import shutil
import subprocess
import time
from ctypes import wintypes
from datetime import datetime
from io import BytesIO

import numpy as np
import psutil
import yaml
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def is_process_running(process_name):
    """Check if a process is running by name."""
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == process_name:
            return True
    return False


def kill_process(process_name):
    """Kill a process by name."""
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == process_name:
            proc.kill()


def wait_for_port(port, timeout=30):
    """Wait for a port to be open."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
        if f":{port}" in result.stdout:
            return True
        time.sleep(1)
    return False


def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)


def read_config(config_file):
    """Read a YAML configuration file."""
    with open(config_file, "r") as file:
        return yaml.safe_load(file)


try:  # Optional Windows-specific dependencies
    import pygetwindow as gw
    import win32api
    import win32con
    import win32gui
    import win32ui
except Exception:  # pragma: no cover - non-Windows environment
    gw = None
    win32gui = None
    win32ui = None
    win32con = None
    win32api = None


def take_window_screenshot(window_title, save_dir, function_type):
    """
    Capture a screenshot of the specified window and save it to ``save_dir``.

    :param window_title: Title of the window
    :param save_dir: Directory to store the screenshot
    :param function_type: Function type (block, freeze, allow)
    :return: Path to the saved screenshot
    """
    if gw is None or win32gui is None:
        raise RuntimeError(
            "Window screenshot functionality requires Windows dependencies"
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{function_type}_{timestamp}.png"
    save_path = os.path.join(save_dir, filename)
    try:
        # Locate the window handle
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"No window found with title containing '{window_title}'")
            raise Exception(f"No window found with title containing '{window_title}'")

        window = windows[0]  # Use the first matching window
        # if not window.isActive:
        #     window.activate()
        #     win32gui.SetForegroundWindow(window._hWnd)

        hwnd = window._hWnd

        # Get the window device context
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bottom - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        # Use ctypes to call PrintWindow
        PW_RENDERFULLCONTENT = 2
        result = ctypes.windll.user32.PrintWindow(
            hwnd, saveDC.GetSafeHdc(), PW_RENDERFULLCONTENT
        )

        if not result:
            logging.error("Failed to capture window screenshot")
            raise Exception("Failed to capture window screenshot")

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        img = Image.frombuffer(
            "RGB",
            (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
            bmpstr,
            "raw",
            "BGRX",
            0,
            1,
        )

        img.save(save_path)
        logging.info(f"Screenshot saved to {save_path}")

        # Cleanup
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

    except Exception as e:
        logging.error(f"Failed to take window screenshot: {e}")
        raise
    return save_path


def compare_images_ssim(reference_path, screenshot_path):
    """Compare two images and return their SSIM similarity score."""
    ref_img = Image.open(reference_path).convert("L")
    scr_img = Image.open(screenshot_path).convert("L")

    ref_arr = np.array(ref_img)
    scr_arr = np.array(scr_img)

    if ref_arr.shape != scr_arr.shape:
        scr_img = scr_img.resize(ref_img.size)
        scr_arr = np.array(scr_img)

    score = ssim(ref_arr, scr_arr)
    return float(score)


def create_run_directory():
    """Create a unique run directory to store screenshots for this test."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    runs_dir = os.path.join(project_root, "test_runs")
    os.makedirs(runs_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(runs_dir, f"run_{timestamp}")
    os.makedirs(run_dir)
    return run_dir


def archive_old_runs(max_runs=10):
    """
    Archive old test runs, keeping only the most recent ones.

    :param max_runs: Maximum number of runs to keep
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    runs_dir = os.path.join(project_root, "test_runs")
    archive_dir = os.path.join(project_root, "archived_runs")

    if not os.path.exists(runs_dir):
        return

    runs = sorted(
        [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))],
        reverse=True,
    )

    if len(runs) > max_runs:
        for old_run in runs[max_runs:]:
            old_run_path = os.path.join(runs_dir, old_run)
            archive_path = os.path.join(archive_dir, old_run)
            os.makedirs(archive_dir, exist_ok=True)
            shutil.move(old_run_path, archive_path)
            logging.info(f"Archived old run: {old_run}")
