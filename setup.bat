@echo off
chcp 65001 > nul

echo Подготовка к установке...

:: Проверяем наличие Python
python --version > nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не установлен!
    echo Пожалуйста, установите Python 3.10 или новее
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Проверяем версию Python
python -c "import sys; assert sys.version_info >= (3,10)" > nul 2>&1
if errorlevel 1 (
    echo Ошибка: Требуется Python 3.10 или новее!
    echo Текущая версия:
    python --version
    pause
    exit /b 1
)

echo.
echo Удаление старого окружения...
if exist venv (
    rmdir /s /q venv
)

echo.
echo Создание нового виртуального окружения...
python -m venv venv

echo.
echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo.
echo Обновление pip...
python -m pip install --upgrade pip

echo.
echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo Обновление yt-dlp до последней версии...
pip install -U yt-dlp

:: Создаем необходимые папки
echo.
echo Создание структуры папок...
if not exist logs mkdir logs
if not exist downloads mkdir downloads

:: Скачиваем ffmpeg если его нет
if not exist ffmpeg.exe (
    echo.
    echo Скачивание ffmpeg...
    curl -L "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" -o "ffmpeg.zip"
    echo Распаковка ffmpeg...
    powershell -Command "Expand-Archive -Force 'ffmpeg.zip' -DestinationPath 'temp'"
    copy "temp\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "ffmpeg.exe"
    rmdir /s /q temp
    del ffmpeg.zip
)

echo.
echo Проверка установки...
python -c "import yt_dlp" > nul 2>&1
if errorlevel 1 (
    echo Ошибка: Не удалось установить yt-dlp!
    pause
    exit /b 1
)

echo.
echo Установка завершена!
echo.
echo Для запуска программы используйте run.bat
pause