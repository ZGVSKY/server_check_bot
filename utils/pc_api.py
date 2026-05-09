import aiohttp
from typing import Dict, Any
import logging

class PCService:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url

    async def shutdown(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/v1/shutdown") as resp:
                    return resp.status == 200
        except Exception as e:
            logging.error(f"API Shutdown Error: {e}")
            return False

    async def reboot(self) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/v1/reboot") as resp:
                    return resp.status == 200
        except Exception as e:
            logging.error(f"API Reboot Error: {e}")
            return False

    async def set_volume(self, action: str) -> bool:
        # action: "up", "down", "mute"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/v1/volume", json={"action": action}) as resp:
                    return resp.status == 200
        except Exception as e:
            logging.error(f"API Volume Error: {e}")
            return False

    async def take_screenshot(self) -> str:
        # Returns path to the temporarily saved image or empty string
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/v1/screenshot") as resp:
                    if resp.status == 200:
                        import os
                        os.makedirs("temp", exist_ok=True)
                        file_path = os.path.join("temp", "bot_screenshot.png")
                        with open(file_path, "wb") as f:
                            f.write(await resp.read())
                        return file_path
        except Exception as e:
            logging.error(f"API Screenshot Error: {e}")
        return ""

    async def get_stats(self) -> Dict[str, Any]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/v1/stats") as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            logging.error(f"API Stats Error: {e}")
            
        # Fallback values if API is offline
        return {
            "cpu_usage": 0,
            "ram_usage": 0,
            "temp": 0,
            "uptime": "N/A"
        }

    async def execute_command(self, command: str) -> str:
        # ... (код вище)

    async def launch_app(self, path: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.base_url}/api/v1/launch", json={"path": path}) as resp:
                    return resp.status == 200
        except Exception as e:
            logging.error(f"API Launch Error: {e}")
            return False

pc_service = PCService()
