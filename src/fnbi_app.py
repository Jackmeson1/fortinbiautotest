import psutil
from pywinauto import Application
import time
import logging
import subprocess

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FNBIApp:
    def __init__(self, app_path):
        self.app_path = app_path
        self.app = None
        self.gui_app = None
        self.service_pid = None
        self.main_window = None

    def start(self):
        logger.info(f"Attempting to start {self.app_path}")
        self.app = Application(backend="uia").start(self.app_path)
        logger.info(f"Application started with PID: {self.app.process}")

        time.sleep(10)  # 给应用程序更多时间来启动所有组件

        self._connect_to_processes()
        self.find_main_window()
        self.print_window_info()

    def _connect_to_processes(self):
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'] == 'FortiNBI.exe':
                    self.app = Application(backend="uia").connect(process=proc.info['pid'], timeout=20)
                    logger.info(f"Connected to FortiNBI.exe with PID: {proc.info['pid']}")
                elif proc.info['name'] == 'FortiNBIGui.exe':
                    self.gui_app = Application(backend="uia").connect(process=proc.info['pid'], timeout=20)
                    logger.info(f"Connected to FortiNBIGui.exe with PID: {proc.info['pid']}")
                elif proc.info['name'] == 'FortiNBIService.exe':
                    self.service_pid = proc.info['pid']
                    logger.info(f"FortiNBIService.exe found with PID: {self.service_pid}")
            except Exception as e:
                logger.error(f"Error connecting to {proc.info['name']}: {e}")

    def find_main_window(self):
        apps_to_check = [self.app, self.gui_app]
        for app in apps_to_check:
            if app:
                try:
                    self.main_window = app.window(title="FortiNBI")
                    logger.info(f"Found main window: {self.main_window.window_text()}")
                    return
                except Exception as e:
                    logger.error(f"Error finding window in {app.process}: {e}")

        logger.warning("Could not find main window in any of the connected applications")

    def is_isolator_running(self):
        if self.main_window:
            try:
                isolator_status = self.main_window.child_window(title="Isolator").window_text()
                logger.info(f"Isolator status: {isolator_status}")
                return "Running" in isolator_status
            except Exception as e:
                logger.error(f"Error checking isolator status: {e}")

        # 检查 WSL 状态
        try:
            result = subprocess.run(["wsl", "-l", "-v"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "fortinbi-isolator" in line:
                    status = line.split()[1]
                    logger.info(f"WSL fortinbi-isolator status: {status}")
                    return status.lower() == "running"
        except Exception as e:
            logger.error(f"Error checking WSL status: {e}")

        return False

    def wait_for_isolator(self, target_state, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_isolator_running() == target_state:
                return True
            time.sleep(5)
        return False

    def print_window_info(self):
        if self.main_window:
            logger.info("\nMain window details:")
            logger.info(f"Title: {self.main_window.window_text()}")
            logger.info(f"Class: {self.main_window.class_name()}")
            logger.info(f"Visible: {self.main_window.is_visible()}")
            logger.info(f"Enabled: {self.main_window.is_enabled()}")
            logger.info("Child windows:")
            for child in self.main_window.children():
                logger.info(f"- {child.window_text()} ({child.class_name()})")
        else:
            logger.warning("\nMain window not found or not accessible")

    def is_running(self):
        return any([self.app, self.gui_app, self.service_pid])

    def get_status(self):
        if self.main_window:
            status_items = self.main_window.children(control_type="Text")
            statuses = [item.window_text() for item in status_items if item.window_text()]
            return "\n".join(statuses)
        return "Status not available"

    import psutil
    import time
    import subprocess

    def close(self):
        # 首先尝试优雅地关闭主窗口
        if self.main_window and self.main_window.exists():
            try:
                self.main_window.close()
                logger.info("Sent close signal to main window")
            except Exception as e:
                logger.error(f"Error closing main window: {e}")

        # 等待一段时间，让应用有机会自行关闭
        time.sleep(5)

        # 只关闭 FortiNBI.exe 和 FortiNBIGui.exe
        processes_to_close = ['FortiNBI.exe', 'FortiNBIGui.exe']
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.info['name'] in processes_to_close:
                try:
                    p = psutil.Process(proc.info['pid'])
                    p.terminate()
                    logger.info(f"Terminated {proc.info['name']} (PID: {proc.info['pid']})")
                except Exception as e:
                    logger.error(f"Error terminating {proc.info['name']} (PID: {proc.info['pid']}): {e}")

        # 等待进程终止
        def wait_for_processes(timeout=10):
            end_time = time.time() + timeout
            while time.time() < end_time:
                if not any(proc.info['name'] in processes_to_close for proc in psutil.process_iter(['name'])):
                    return True
                time.sleep(0.5)
            return False

        if not wait_for_processes():
            logger.warning("Some processes did not terminate gracefully. Forcing termination.")
            for proc in psutil.process_iter(['name', 'pid']):
                if proc.info['name'] in processes_to_close:
                    try:
                        p = psutil.Process(proc.info['pid'])
                        p.kill()
                        logger.info(f"Forcefully killed {proc.info['name']} (PID: {proc.info['pid']})")
                    except Exception as e:
                        logger.error(f"Error killing {proc.info['name']} (PID: {proc.info['pid']}): {e}")

        # 关闭 isolator
        if self.is_isolator_running():
            try:
                subprocess.run(["wsl", "--terminate", "fortinbi-isolator"], check=True)
                logger.info("Terminated fortinbi-isolator WSL instance")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error terminating fortinbi-isolator: {e}")

        # 重置相关类属性
        self.app = None
        self.gui_app = None
        self.main_window = None

        # 记录 FortiNBIService.exe 的状态
        service_running = any(proc.info['name'] == 'FortiNBIService.exe' for proc in psutil.process_iter(['name']))
        if service_running:
            logger.info("FortiNBIService.exe is still running as intended")
        else:
            logger.warning("FortiNBIService.exe is not running. This might be unexpected.")

        logger.info("FNBI components (except service) have been closed")