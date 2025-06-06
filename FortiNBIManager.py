import subprocess
import psutil
from src.utils import read_config
import os


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
    def start_process(path_to_exe):
        subprocess.Popen(path_to_exe)


if __name__ == '__main__':
    manager = FortiNBIManager()
    project_root = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    cfg = read_config(config_path)

    if not manager.is_process_running('FortiNBI.exe'):
        print("FortiNBI.exe is not running. Starting it now...")
        manager.start_process(cfg['fnbi']['executable_path'])
    else:
        print("FortiNBI.exe is already running.")
