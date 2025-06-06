# src/fnbi_service.py
import subprocess
import time


class FNBIService:
    def __init__(self, service_name="FortiNBI.rating_service"):
        self.service_name = service_name

    def start(self):
        subprocess.run(["sc", "start", self.service_name], check=True)
        time.sleep(5)  # Wait for service to fully start

    def stop(self):
        subprocess.run(["sc", "stop", self.service_name], check=True)
        time.sleep(5)  # Wait for service to fully stop

    def restart(self):
        self.stop()
        self.start()

    def is_running(self):
        result = subprocess.run(
            ["sc", "query", self.service_name], capture_output=True, text=True
        )
        return "RUNNING" in result.stdout

    def get_status(self):
        result = subprocess.run(
            [
                "powershell",
                f"Get-Service -Name '{self.service_name}' | Select-Object Status, Name, DisplayName | Format-List",
            ],
            capture_output=True,
            text=True,
        )
        return result.stdout

    def get_detailed_status(self):
        result = subprocess.run(
            ["sc", "query", self.service_name], capture_output=True, text=True
        )
        return result.stdout
