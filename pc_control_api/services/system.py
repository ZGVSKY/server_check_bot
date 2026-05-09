import psutil
import os
import subprocess
import pyautogui
from typing import Dict, Any

class SystemService:
    @staticmethod
    def shutdown() -> bool:
        try:
            if os.name == 'nt':
                os.system('shutdown /s /t 1')
            else:
                os.system('shutdown -h now')
            return True
        except Exception:
            return False

    @staticmethod
    def reboot() -> bool:
        try:
            if os.name == 'nt':
                os.system('shutdown /r /t 1')
            else:
                os.system('reboot')
            return True
        except Exception:
            return False

    @staticmethod
    def get_stats() -> Dict[str, Any]:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        
        # Temperature (basic mock or try to get)
        temp = 0
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps and 'coretemp' in temps:
                temp = temps['coretemp'][0].current
        
        # Uptime
        boot_time = psutil.boot_time()
        import time
        uptime_seconds = time.time() - boot_time
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        uptime = f"{int(hours)}h {int(minutes)}m"

        return {
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "temp": temp,
            "uptime": uptime
        }

    @staticmethod
    def set_volume(action: str) -> bool:
        try:
            if os.name == 'nt':
                if action == "up":
                    cmd = "$obj = new-object -com wscript.shell; $obj.SendKeys([char]175)"
                elif action == "down":
                    cmd = "$obj = new-object -com wscript.shell; $obj.SendKeys([char]174)"
                elif action == "mute":
                    cmd = "$obj = new-object -com wscript.shell; $obj.SendKeys([char]173)"
                else:
                    return False
                subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            return True
        except Exception:
            return False

    @staticmethod
    def take_screenshot(save_path: str) -> bool:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            return True
        except Exception:
            return False

system_service = SystemService()
