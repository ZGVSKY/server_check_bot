from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.system import system_service
import os

router = APIRouter(prefix="/api/v1", tags=["PC Control"])

class VolumeRequest(BaseModel):
    action: str  # "up", "down", "mute"

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
        raise HTTPException(status_code=400, detail="Invalid action. Use 'up', 'down', or 'mute'.")
    
    if system_service.set_volume(req.action):
        return {"status": "success", "message": f"Volume {req.action} executed"}
    raise HTTPException(status_code=500, detail="Failed to change volume")

@router.get("/screenshot")
async def get_screenshot():
    # Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", "screenshot.png")
    
    if system_service.take_screenshot(file_path):
        return FileResponse(file_path, media_type="image/png", filename="screenshot.png")
    raise HTTPException(status_code=500, detail="Failed to take screenshot")
