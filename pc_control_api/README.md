# PC Control API

Це REST API, написане на **FastAPI**, яке безпосередньо взаємодіє з комп'ютером (отримує статистику, робить скріншоти, керує живленням та гучністю). Телеграм-бот надсилає запити сюди.

## 🚀 Ендпоінти
- `GET /api/v1/stats`: Отримати показники системи (CPU, RAM, Temp, Uptime).
- `GET /api/v1/screenshot`: Отримати скріншот екрана (повертає PNG).
- `POST /api/v1/shutdown`: Вимкнути комп'ютер.
- `POST /api/v1/reboot`: Перезавантажити комп'ютер.
- `POST /api/v1/volume`: Змінити гучність. Тіло запиту: `{"action": "up" | "down" | "mute"}`

## 🛠 Встановлення та запуск

1. Перейдіть до папки API:
   ```bash
   cd pc_control_api
   ```
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустіть сервер:
   ```bash
   python main.py
   ```
   Або за допомогою uvicorn безпосередньо:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
   ```

Після запуску ви зможете переглянути інтерактивну документацію (Swagger) за адресою: `http://localhost:5000/docs`.
