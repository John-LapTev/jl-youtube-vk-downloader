@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo Проверка обновлений...

:: Создаем временную папку
if exist temp rmdir /s /q temp
mkdir temp
cd temp

:: Скачиваем актуальные файлы для проверки
echo Загрузка информации об обновлениях...
curl -L "https://github.com/John-LapTev/jl-youtube-vk-downloader/archive/main.zip" -o main.zip

:: Распаковываем во временную папку
echo Проверка доступных обновлений...
powershell -Command "Expand-Archive -Force 'main.zip' -DestinationPath '.'"

:: Создаем список файлов для обновления
echo.
echo Доступны следующие обновления:
echo -------------------------------
cd jl-youtube-vk-downloader-main

:: Проверяем обычные файлы
for %%F in (*.*) do (
    if exist "..\..\%%F" (
        fc /b "%%F" "..\..\%%F" >nul 2>&1
        if errorlevel 1 (
            echo Будет обновлен: %%F
            set "has_updates=1"
        )
    ) else (
        echo Будет добавлен: %%F
        set "has_updates=1"
    )
)

:: Проверяем папки (кроме venv)
for /d %%D in (*) do (
    if not "%%D"=="venv" (
        if not exist "..\..\%%D" (
            echo Будет добавлена папка: %%D
            set "has_updates=1"
        )
    )
)

echo -------------------------------

:: Проверяем, есть ли обновления
if not defined has_updates (
    echo.
    echo Обновления не требуются.
    goto CLEANUP
)

:: Спрашиваем подтверждение на обновление
echo.
choice /c YN /n /m "Установить эти обновления? (Y/N) "
if errorlevel 2 goto CANCEL_UPDATE

:: Если пользователь согласился, выполняем обновление
echo.
echo Установка обновлений...

:: Копируем файлы
for %%F in (*.*) do (
    if exist "..\..\%%F" (
        fc /b "%%F" "..\..\%%F" >nul 2>&1
        if errorlevel 1 (
            echo Обновление: %%F
            copy /y "%%F" "..\.." >nul 2>&1
        )
    ) else (
        echo Добавление: %%F
        copy /y "%%F" "..\.." >nul 2>&1
    )
)

:: Копируем папки
for /d %%D in (*) do (
    if not "%%D"=="venv" (
        if exist "..\..\%%D" (
            xcopy /s /y /d "%%D" "..\..\%%D" >nul 2>&1
        ) else (
            echo Добавление папки: %%D
            xcopy /s /y "%%D" "..\..\%%D" >nul 2>&1
        )
    )
)

echo.
echo Обновление успешно завершено!
echo.
echo ВНИМАНИЕ: Если программа не запускается после обновления,
echo запустите setup.bat для переустановки зависимостей.
goto CLEANUP

:CANCEL_UPDATE
echo.
echo Обновление отменено.

:CLEANUP
:: Очищаем временные файлы
cd ..
rmdir /s /q temp

echo.
pause

endlocal