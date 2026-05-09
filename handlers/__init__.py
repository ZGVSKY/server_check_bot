from .common import router as common_router
from .pc_control import router as pc_router
from .auth import router as auth_router
from .apps import router as apps_router

# Export all routers
routers = [auth_router, common_router, pc_router, apps_router]
