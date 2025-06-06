import subprocess
import psutil
import time


class FortiNBIManager:

    @staticmethod
    def is_process_running(process_name):
        try:
            # 遍历所有的运行中的进程
            for proc in psutil.process_iter():
                # 获取进程详情作为字典
                process_info = proc.as_dict(attrs=['pid', 'name', 'create_time'])
                # 检查进程名是否匹配
                if process_name.lower() in process_info['name'].lower():
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



if __name__ == '__main__':
    manager = FortiNBIManager()

    # \u66ff\u6362\u6210\u4f60\u7684 FortiNBI.exe \u7684\u5b8c\u6574\u8def\u5f84
    path_to_forti_nbi = r"C:\\Program Files (x86)\\Fortinet\\FortiNBI\\FortiNBI.exe"

    proc = None
    if not manager.is_process_running('FortiNBI.exe'):
        print("FortiNBI.exe is not running. Starting it now...")
        proc = manager.start_process(path_to_forti_nbi)
    else:
        print("FortiNBI.exe is already running.")

    if proc:
        input("Press Enter to terminate FortiNBI...")
        manager.stop_process(proc)
