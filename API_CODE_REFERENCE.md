# Код для API Сервера (PC Control API)

Скопіюйте цей код у відповідні файли вашого API проекту за шляхом `C:\Users\User\PycharmProjects\pc_control_api`.

## 1. services/system.py

```python
import psutil
import os
import subprocess
import pyautogui
from typing import Dict, Any
import time

# Спробуємо імпортувати WMI для Windows (потрібно для температури)
try:
    import wmi
    w = wmi.WMI(namespace="root\\wmi")
except Exception:
    w = None

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
        
        temp = 0
        # Спроба зчитати через WMI (Windows)
        if os.name == 'nt' and w:
            try:
                temp_info = w.MSAcpi_ThermalZoneTemperature()
                if temp_info:
                    # Конвертація з десятих часток Кельвіна в Цельсій
                    temp = int((temp_info[0].CurrentTemperature / 10.0) - 273.15)
            except Exception:
                pass
        
        # Якщо WMI не спрацював, пробуємо psutil
        if temp <= 0 and hasattr(psutil, "sensors_temperatures"):
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            temp = int(entries[0].current)
                            break
            except Exception:
                pass
        
        boot_time = psutil.boot_time()
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

    @staticmethod
    def execute_command(command: str) -> str:
        try:
            import subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = f"Команда виконана (код: {result.returncode})"
            return output
        except Exception as e:
            return f"Помилка при виконанні: {str(e)}"

    @staticmethod
    def launch_app(path: str) -> bool:
        try:
            os.startfile(path)
            return True
        except Exception:
            return False

# Цей рядок має бути в самому кінці БЕЗ відступів
system_service = SystemService()
```

## 2. routers/control.py

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.system import system_service
import os

router = APIRouter(prefix="/api/v1", tags=["PC Control"])

class VolumeRequest(BaseModel):
    action: str  # "up", "down", "mute"

class CommandRequest(BaseModel):
    command: str

class LaunchRequest(BaseModel):
    path: str

@router.post("/shutdown")
async def shutdown_pc():
    if system_service.shutdown():
        return {"status": "success", "message": "Shutting down..."}
    raise HTTPException(status_code=500, detail="Failed to initiate shutdown")

@router.post("/reboot")
async def reboot_pc():
    if system_service.reboot():
        return {"status": "success", "message": "Rebooting..."}
    raise HTTPException(status_code=500, detail="Failed to initiate reboot")

@router.get("/stats")
async def get_stats():
    return system_service.get_stats()

@router.post("/volume")
async def set_volume(req: VolumeRequest):
    if req.action not in ["up", "down", "mute"]:
        raise HTTPException(status_code=400, detail="Invalid action.")
    
    if system_service.set_volume(req.action):
        return {"status": "success", "message": f"Volume {req.action} executed"}
    raise HTTPException(status_code=500, detail="Failed to change volume")

@router.get("/screenshot")
async def get_screenshot():
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", "screenshot.png")
    
    if system_service.take_screenshot(file_path):
        return FileResponse(file_path, media_type="image/png", filename="screenshot.png")
    raise HTTPException(status_code=500, detail="Failed to take screenshot")

@router.post("/execute")
async def execute_cmd(req: CommandRequest):
    output = system_service.execute_command(req.command)
    return {"status": "success", "output": output}

@router.post("/launch")
async def launch_app(req: LaunchRequest):
    if system_service.launch_app(req.path):
        return {"status": "success", "message": "App launched"}
    raise HTTPException(status_code=500, detail="Failed to launch app")
```
