
@echo off
echo Starting PC Control Telegram Bot...
echo Ensure your .env file is configured!
echo.

:: Перевірка наявності віртуального середовища
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
) else (
    echo Virtual environment not found. Running with system python...
)

python main.py
pause
