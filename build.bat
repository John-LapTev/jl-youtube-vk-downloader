@echo off
chcp 65001 > nul

:: Переходим в директорию проекта
cd /d "%~dp0"

echo Текущая директория: %CD%
echo Подготовка к сборке...

:: Проверяем наличие виртуального окружения
if not exist venv (
    echo Ошибка: Виртуальное окружение не найдено!
    echo Пожалуйста, сначала запустите setup.bat
    pause
    exit /b 1
)

:: Проверяем и создаем все необходимые папки
echo Создание папок...
if exist "build" (
    echo Удаляем старую папку build...
    rmdir /s /q "build"
)
echo Создаем папку build...
mkdir "build"

if exist "dist" (
    echo Удаляем старую папку dist...
    rmdir /s /q "dist"
)
echo Создаем папку dist...
mkdir "dist"

if exist "src\resources" (
    echo Удаляем старую папку resources...
    rmdir /s /q "src\resources"
)
echo Создаем папку resources...
mkdir "src\resources"

:: Активируем виртуальное окружение
call venv\Scripts\activate.bat

:: Устанавливаем/обновляем инструменты сборки
echo Установка инструментов сборки...
pip install -U pyinstaller

:: Определяем пути к пакетам
echo Определение путей...
for /f "tokens=*" %%i in ('python -c "import customtkinter; print(customtkinter.__path__[0])"') do set CTK_PATH=%%i
for /f "tokens=*" %%i in ('python -c "import yt_dlp; print(yt_dlp.__path__[0])"') do set YTDLP_PATH=%%i

:: Абсолютный путь к иконке и ffmpeg
set ICON_PATH=%CD%\src\assets\icon.ico
set FFMPEG_PATH=%CD%\ffmpeg.exe

:: Проверяем наличие ffmpeg
if not exist "%FFMPEG_PATH%" (
    echo Скачивание ffmpeg...
    curl -L "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" -o "build\ffmpeg.zip"
    powershell -Command "Expand-Archive -Force 'build\ffmpeg.zip' -DestinationPath 'build'"
    copy "build\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "%FFMPEG_PATH%"
)

:: Копируем ffmpeg в ресурсы
copy "%FFMPEG_PATH%" "src\resources\ffmpeg.exe"

:: Создаем файлы Python для работы с ресурсами
echo import os, sys, tempfile, ssl> "src\resources\extract_ffmpeg.py"
echo.>> "src\resources\extract_ffmpeg.py"
echo # Отключаем проверку SSL для Python>> "src\resources\extract_ffmpeg.py"
echo if hasattr(ssl, '_create_unverified_context'):>> "src\resources\extract_ffmpeg.py"
echo     ssl._create_default_https_context = ssl._create_unverified_context>> "src\resources\extract_ffmpeg.py"
echo.>> "src\resources\extract_ffmpeg.py"
echo def get_ffmpeg_path():>> "src\resources\extract_ffmpeg.py"
echo     if getattr(sys, 'frozen', False):>> "src\resources\extract_ffmpeg.py"
echo         temp_dir = tempfile._get_default_tempdir()>> "src\resources\extract_ffmpeg.py"
echo         ffmpeg_path = os.path.join(temp_dir, 'ffmpeg.exe')>> "src\resources\extract_ffmpeg.py"
echo         if not os.path.exists(ffmpeg_path):>> "src\resources\extract_ffmpeg.py"
echo             with open(os.path.join(sys._MEIPASS, 'ffmpeg.exe'), 'rb') as f_src:>> "src\resources\extract_ffmpeg.py"
echo                 with open(ffmpeg_path, 'wb') as f_dst:>> "src\resources\extract_ffmpeg.py"
echo                     f_dst.write(f_src.read())>> "src\resources\extract_ffmpeg.py"
echo         return ffmpeg_path>> "src\resources\extract_ffmpeg.py"
echo     return 'ffmpeg.exe'>> "src\resources\extract_ffmpeg.py"

echo.> "src\resources\__init__.py"

:: Задаем имена программы (временное и финальное)
set TEMP_NAME=JL-YT-VK-Downloader
set FINAL_NAME=JL YouTube ^& VK Video Downloader

:: Собираем приложение
echo Сборка приложения...
pyinstaller --clean ^
           --name "%TEMP_NAME%" ^
           --windowed ^
           --onefile ^
           --icon="%ICON_PATH%" ^
           --add-data "%CTK_PATH%;customtkinter/" ^
           --add-data "%YTDLP_PATH%;yt_dlp/" ^
           --add-data "%FFMPEG_PATH%;." ^
           --hidden-import "customtkinter" ^
           --hidden-import "PIL" ^
           --hidden-import "PIL._tkinter_finder" ^
           --hidden-import "yt_dlp.utils" ^
           --hidden-import "yt_dlp.extractor" ^
           --hidden-import "asyncio" ^
           --hidden-import "aiohttp" ^
           --collect-submodules "yt_dlp" ^
           --collect-data "yt_dlp" ^
           --workpath "build" ^
           --distpath "dist" ^
           --specpath "build" ^
           "src\main.py"

:: Проверяем результат сборки
if not exist "dist\%TEMP_NAME%.exe" (
    echo ОШИБКА: Сборка не удалась! Файл exe не создан!
    pause
    exit /b 1
)

:: Переименовываем файл
echo.
echo Переименование файла...
ren "dist\%TEMP_NAME%.exe" "%FINAL_NAME%.exe"

echo.
echo Копирование дополнительных файлов...
:: Создаем папки для логов и загрузок
mkdir "dist\logs"
mkdir "dist\downloads"

:: Очистка временных файлов
echo Очистка временных файлов...
rmdir /s /q "build"
rmdir /s /q "src\resources"

echo.
echo Сборка успешно завершена!
echo Ваш файл находится в папке dist/
echo.
pause