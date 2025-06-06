import psutil
import subprocess
import time

def is_process_running(process_name):
    """Check if a process is running by name."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def kill_process(process_name):
    """Kill a process by name."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
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
    import yaml
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)


# /src/utils.py

import os
import logging
from PIL import Image
from io import BytesIO
from skimage.metrics import structural_similarity as ssim
import numpy as np

try:  # Optional Windows-specific dependencies
    import pygetwindow as gw
    import win32gui
    import win32ui
    import win32con
    import win32api
except Exception:  # pragma: no cover - non-Windows environment
    gw = None
    win32gui = None
    win32ui = None
    win32con = None
    win32api = None


import ctypes
from ctypes import wintypes

def take_window_screenshot(window_title, save_dir, function_type):
    """
    对指定窗口进行截图并保存到指定目录。

    :param window_title: 窗口的标题
    :param save_dir: 保存截图的目录
    :param function_type: 功能类型（block, freeze, allow）
    :return: 保存的截图路径
    """
    if gw is None or win32gui is None:
        raise RuntimeError("Window screenshot functionality requires Windows dependencies")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{function_type}_{timestamp}.png"
    save_path = os.path.join(save_dir, filename)
    try:
        # 查找窗口句柄
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"No window found with title containing '{window_title}'")
            raise Exception(f"No window found with title containing '{window_title}'")

        window = windows[0]  # 选择第一个匹配的窗口
        # if not window.isActive:
        #     window.activate()
        #     win32gui.SetForegroundWindow(window._hWnd)

        hwnd = window._hWnd

        # 获取窗口的设备上下文
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bottom - top

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        # 使用 ctypes 调用 PrintWindow
        PW_RENDERFULLCONTENT = 2
        result = ctypes.windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), PW_RENDERFULLCONTENT)

        if not result:
            logging.error("Failed to capture window screenshot")
            raise Exception("Failed to capture window screenshot")

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1
        )

        img.save(save_path)
        logging.info(f"Screenshot saved to {save_path}")

        # 清理
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


import os
import logging
from datetime import datetime
import shutil


def create_run_directory():
    """
    创建一个唯一的运行目录来存储本次测试的截图。
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    runs_dir = os.path.join(project_root, 'test_runs')
    os.makedirs(runs_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(runs_dir, f"run_{timestamp}")
    os.makedirs(run_dir)
    return run_dir



def archive_old_runs(max_runs=10):
    """
    存档旧的测试运行，只保留最新的几次运行。

    :param max_runs: 要保留的最大运行次数
    """
    project_root = os.path.dirname(os.path.dirname(__file__))
    runs_dir = os.path.join(project_root, 'test_runs')
    archive_dir = os.path.join(project_root, 'archived_runs')

    if not os.path.exists(runs_dir):
        return

    runs = sorted([d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))], reverse=True)

    if len(runs) > max_runs:
        for old_run in runs[max_runs:]:
            old_run_path = os.path.join(runs_dir, old_run)
            archive_path = os.path.join(archive_dir, old_run)
            os.makedirs(archive_dir, exist_ok=True)
            shutil.move(old_run_path, archive_path)
            logging.info(f"Archived old run: {old_run}")
