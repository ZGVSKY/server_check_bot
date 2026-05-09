import asyncio
import logging
from aiogram import Bot
from config import config
from utils.pc_api import pc_service

async def monitor_pc(bot: Bot):
    logging.info("Monitoring task started.")
    while True:
        try:
            stats = await pc_service.get_stats()
            current_temp = stats.get("temp", 0)
            
            if current_temp > config.temp_threshold:
                await bot.send_message(
                    config.admin_id,
                    f"⚠️ **УВАГА: ПЕРЕГРІВ!**\nПоточна температура: {current_temp}°C\n"
                    f"Поріг: {config.temp_threshold}°C"
                )
                logging.warning(f"Overheat detected: {current_temp}°C")
            
        except Exception as e:
            logging.error(f"Error in monitoring task: {e}")
        
        # Перевірка кожні 60 секунд
        await asyncio.sleep(60)
