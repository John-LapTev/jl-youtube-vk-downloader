@echo off
chcp 65001 > nul

:: Проверяем наличие виртуального окружения
if not exist venv (
    echo Ошибка: Виртуальное окружение не найдено!
    echo Пожалуйста, сначала запустите setup.bat
    pause
    exit /b 1
)

:: Проверяем наличие ffmpeg
if not exist ffmpeg.exe (
    echo Ошибка: Не найден ffmpeg.exe!
    echo Пожалуйста, запустите setup.bat
    pause
    exit /b 1
)

:: Активируем виртуальное окружение и запускаем программу
call venv\Scripts\activate.bat
python src\main.py
pause