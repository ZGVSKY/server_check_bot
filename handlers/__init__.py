from .common import router as common_router
from .pc_control import router as pc_router

# Export all routers
routers = [common_router, pc_router]
