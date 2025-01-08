@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: Показываем, где мы находимся
echo Текущая директория: %CD%
echo.

:: Проверяем, что мы в правильной папке
if not exist "setup.bat" (
    echo Ошибка: Скрипт должен быть запущен из корневой папки проекта!
    echo Требуемые файлы не найдены в текущей директории.
    pause
    exit /b 1
)

:: Сохраняем текущую директорию
set "CURRENT_DIR=%CD%"
set "TEMP_DIR=%CD%\temp\jl-youtube-vk-downloader-main"

echo Проверка обновлений...

:: Проверяем и удаляем временную папку
if exist "%CURRENT_DIR%\temp" (
    rmdir /s /q "%CURRENT_DIR%\temp"
    timeout /t 1 /nobreak >nul
)

:: Создаем временную папку
mkdir "%CURRENT_DIR%\temp"
cd "%CURRENT_DIR%\temp"

:: Скачиваем актуальные файлы для проверки
echo Загрузка информации об обновлениях...
curl -L "https://github.com/John-LapTev/jl-youtube-vk-downloader/archive/main.zip" -o main.zip

:: Распаковываем во временную папку
echo Проверка доступных обновлений...
powershell -Command "Expand-Archive -Force 'main.zip' -DestinationPath '.'"

echo.
echo Доступны следующие обновления:
echo -------------------------------

cd jl-youtube-vk-downloader-main

:: Очищаем файл изменений
type nul > ..\changes.txt

:: Проверяем корневые файлы
pushd "%TEMP_DIR%"
for %%F in (*.*) do (
    if exist "%CURRENT_DIR%\%%F" (
        fc /b "%%F" "%CURRENT_DIR%\%%F" >nul 2>&1
        if errorlevel 1 (
            echo Будет обновлен: %%F >> ..\changes.txt
        )
    ) else (
        if not "%%F"=="changes.txt" (
            echo Будет добавлен: %%F >> ..\changes.txt
        )
    )
)

:: Проверяем подпапки рекурсивно
for /d %%D in (*) do (
    if not "%%D"=="venv" if not "%%D:~0,4"==".git" (
        pushd "%%D"
        for /f "delims=" %%F in ('dir /s /b /a-d') do (
            set "FILE_PATH=%%F"
            set "RELATIVE_PATH=!FILE_PATH:%TEMP_DIR%\=!"
            
            if exist "%CURRENT_DIR%\!RELATIVE_PATH!" (
                fc /b "%%F" "%CURRENT_DIR%\!RELATIVE_PATH!" >nul 2>&1
                if errorlevel 1 (
                    echo Будет обновлен: !RELATIVE_PATH! >> ..\..\changes.txt
                )
            ) else (
                echo Будет добавлен: !RELATIVE_PATH! >> ..\..\changes.txt
            )
        )
        popd
    )
)

:: Показываем изменения
type ..\changes.txt
echo -------------------------------

:: Проверяем, есть ли изменения
findstr /r /c:"." ..\changes.txt >nul
if errorlevel 1 (
    echo.
    echo Обновления не требуются.
    echo Нажмите любую клавишу для выхода...
    pause > nul
    goto CLEANUP
)

:: Спрашиваем подтверждение на обновление
echo.
choice /c YN /n /m "Установить эти обновления? (Y/N) "
if errorlevel 2 goto CANCEL_UPDATE

:: Если пользователь согласился, выполняем обновление
echo.
echo Установка обновлений...
echo -------------------------------

:: Обновляем файлы из списка изменений
for /f "usebackq tokens=*" %%L in ("..\changes.txt") do (
    set "line=%%L"
    set "file=!line:~16!"
    
    if "!line:~0,14!"=="Будет обновлен" (
        echo Обновление: !file!
        if not exist "%CURRENT_DIR%\!file!\.." mkdir "%CURRENT_DIR%\!file!\.." 2>nul
        :: Используем PowerShell для правильной обработки кодировки
        powershell -Command "$content = Get-Content '!file!' -Raw; [System.IO.File]::WriteAllText('%CURRENT_DIR%\!file!', $content, [System.Text.Encoding]::UTF8)" >nul 2>&1
    )
    if "!line:~0,14!"=="Будет добавлен" (
        echo Добавление: !file!
        if not exist "%CURRENT_DIR%\!file!\.." mkdir "%CURRENT_DIR%\!file!\.." 2>nul
        :: Используем PowerShell для правильной обработки кодировки
        powershell -Command "$content = Get-Content '!file!' -Raw; [System.IO.File]::WriteAllText('%CURRENT_DIR%\!file!', $content, [System.Text.Encoding]::UTF8)" >nul 2>&1
    )
)

echo -------------------------------
echo.
echo ✅ Обновление успешно завершено!
echo.
echo ⚠️ ВНИМАНИЕ:
echo    * Если программа не запускается после обновления,
echo    * запустите setup.bat для переустановки зависимостей
echo    * Нажмите любую клавишу для завершения...
echo.
pause > nul
goto CLEANUP

:CANCEL_UPDATE
echo.
echo ❌ Обновление отменено.
echo    Нажмите любую клавишу для выхода...
echo.
pause > nul
goto CLEANUP

:CLEANUP
:: Возвращаемся в исходную директорию и очищаем временные файлы
cd "%CURRENT_DIR%"
if exist temp (
    rmdir /s /q temp
    if exist temp (
        echo.
        echo ⚠️ Не удалось удалить временные файлы.
        echo    Пожалуйста, удалите папку temp вручную.
        echo.
    )
)

:: Финальная пауза перед выходом
timeout /t 3
exit