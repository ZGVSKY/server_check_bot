from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import config
from database.user_db import user_db

class IsSuperuser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == config.admin_id

class HasPermission(BaseFilter):
    def __init__(self, required_permission: str):
        self.required_permission = required_permission

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        
        # Superuser always has access
        if user_id == config.admin_id:
            return True
            
        user = user_db.get_user(str(user_id))
        if not user:
            return False
            
        permission = user.get("permission", "unauthorized")
        
        if self.required_permission == "full":
            return permission == "full"
        if self.required_permission == "stats_only":
            return permission in ["stats_only", "full"]
            
        return False
