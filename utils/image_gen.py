from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict, Any

def create_stats_image(stats: Dict[str, Any], output_path: str = "temp/stats.png"):
    # Переконуємось, що папка temp існує
    os.makedirs("temp", exist_ok=True)
    
    # Розміри картинки
    width, height = 500, 350
    background_color = (24, 24, 27)  # Темно-сірий (Modern UI style)
    text_color = (255, 255, 255)
    accent_color = (59, 130, 246)  # Синій акцент
    
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Заголовок
    draw.text((20, 20), "SYSTEM MONITOR", fill=accent_color)
    draw.line((20, 50, 480, 50), fill=(63, 63, 70), width=2)
    
    y_offset = 80
    
    def draw_stat(label: str, value: str, percent: float = None):
        nonlocal y_offset
        # Текст мітки
        draw.text((30, y_offset), f"{label}:", fill=(161, 161, 170))
        # Значення
        draw.text((150, y_offset), str(value), fill=text_color)
        
        # Якщо є відсоток, малюємо прогрес-бар
        if percent is not None:
            bar_width = 300
            bar_height = 10
            bar_x = 150
            bar_y = y_offset + 25
            
            # Фон бару
            draw.rectangle((bar_x, bar_y, bar_x + bar_width, bar_y + bar_height), fill=(63, 63, 70))
            # Заповнення
            fill_width = int((percent / 100) * bar_width)
            draw.rectangle((bar_x, bar_y, bar_x + fill_width, bar_y + bar_height), fill=accent_color)
            y_offset += 30
            
        y_offset += 50

    draw_stat("CPU Usage", f"{stats.get('cpu_usage', 0)}%", stats.get('cpu_usage'))
    draw_stat("RAM Usage", f"{stats.get('ram_usage', 0)}%", stats.get('ram_usage'))
    draw_stat("Temperature", f"{stats.get('temp', 0)}°C")
    draw_stat("Uptime", stats.get('uptime', 'N/A'))
    
    # Нижній колонтитул
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((20, 320), f"Last updated: {now}", fill=(82, 82, 91))
    
    img.save(output_path)
    return output_path
