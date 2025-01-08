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

echo.
echo Доступны следующие обновления:
echo -------------------------------

cd jl-youtube-vk-downloader-main

:: Создаем временный файл для списка изменений
type nul > ..\changes.txt

:: Проверяем файлы в корневой директории
for %%F in (*.*) do (
    if exist "..\..\%%F" (
        fc /b "%%F" "..\..\%%F" >nul 2>&1
        if errorlevel 1 (
            echo Будет обновлен: %%F >> ..\changes.txt
            set "has_updates=1"
        )
    ) else (
        echo Будет добавлен: %%F >> ..\changes.txt
        set "has_updates=1"
    )
)

:: Рекурсивная проверка всех подпапок
for /f "tokens=*" %%D in ('dir /a:d /b /s') do (
    set "relative_path=%%D"
    set "relative_path=!relative_path:%CD%\=!"
    
    if not "!relative_path!"=="venv" (
        if not "!relative_path:~0,4!"==".git" (
            pushd "%%D"
            for %%F in (*.*) do (
                if exist "..\..\..\!relative_path!\%%F" (
                    fc /b "%%F" "..\..\..\!relative_path!\%%F" >nul 2>&1
                    if errorlevel 1 (
                        echo Будет обновлен: !relative_path!\%%F >> ..\..\changes.txt
                        set "has_updates=1"
                    )
                ) else (
                    echo Будет добавлен: !relative_path!\%%F >> ..\..\changes.txt
                    set "has_updates=1"
                )
            )
            popd
        )
    )
)

:: Показываем изменения
type ..\changes.txt
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

:: Обновляем файлы из списка изменений
for /f "tokens=*" %%L in (..\changes.txt) do (
    set "line=%%L"
    set "file=!line:~16!"
    
    if "!line:~0,14!"=="Будет обновлен" (
        echo Обновление: !file!
        copy /y "!file!" "..\..\!file!" >nul 2>&1
    )
    if "!line:~0,14!"=="Будет добавлен" (
        echo Добавление: !file!
        if not exist "..\..\!file!\.." mkdir "..\..\!file!\.." 2>nul
        copy /y "!file!" "..\..\!file!" >nul 2>&1
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