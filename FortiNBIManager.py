import subprocess

import psutil
import time

from src.utils import read_config
import os



class FortiNBIManager:

    @staticmethod
    def is_process_running(process_name):
        try:
            # Iterate over all running processes
            for proc in psutil.process_iter():
                # Retrieve process information as a dictionary
                process_info = proc.as_dict(attrs=["pid", "name", "create_time"])
                # Check whether the process name matches
                if process_name.lower() in process_info["name"].lower():
                    return True
            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False

    @staticmethod
    def start_process(path_to_exe, timeout=30):
        """Launch FortiNBI and wait for it to start.

        Returns the ``subprocess.Popen`` object for the launched process.
        """
        proc = subprocess.Popen(path_to_exe)
        start_time = time.time()
        while time.time() - start_time < timeout:
            if proc.poll() is None and FortiNBIManager.is_process_running('FortiNBI.exe'):
                return proc
            time.sleep(0.5)
        raise RuntimeError('FortiNBI.exe did not start successfully')

    @staticmethod
    def stop_process(proc, timeout=10):
        """Terminate the given process and verify it has exited."""
        if proc is None:
            return True
        proc.terminate()
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=timeout)
        return proc.poll() is not None and not FortiNBIManager.is_process_running('FortiNBI.exe')



if __name__ == "__main__":
    manager = FortiNBIManager()

    project_root = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)


    proc = None
    if not manager.is_process_running('FortiNBI.exe'):

        print("FortiNBI.exe is not running. Starting it now...")

        manager.start_process(cfg['fnbi']['executable_path'])

    else:
        print("FortiNBI.exe is already running.")

    if proc:
        input("Press Enter to terminate FortiNBI...")
        manager.stop_process(proc)
