@echo off
chcp 65001 > nul

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
for /f "delims=" %%F in ('dir /b /a-d') do (
    if exist "..\..\%%F" (
        fc /b "%%F" "..\..\%%F" > nul
        if errorlevel 1 (
            echo Будет обновлен: %%F
        )
    ) else (
        echo Будет добавлен: %%F
    )
)

:: Проверяем папки
for /f "delims=" %%D in ('dir /b /ad') do (
    if not "%%D"=="venv" (
        if not exist "..\..\%%D" (
            echo Будет добавлена папка: %%D
        )
    )
)

cd ..
echo -------------------------------
echo.

:: Спрашиваем подтверждение на обновление
choice /c YN /n /m "Установить эти обновления? (Y/N) "
if errorlevel 2 goto CANCEL_UPDATE

:: Если пользователь согласился, выполняем обновление
cd jl-youtube-vk-downloader-main
echo.
echo Установка обновлений...
for /f "delims=" %%F in ('dir /b /a-d') do (
    if exist "..\..\%%F" (
        fc /b "%%F" "..\..\%%F" > nul
        if errorlevel 1 (
            echo Обновление: %%F
            copy /y "%%F" "..\.." > nul
        )
    ) else (
        echo Добавление: %%F
        copy /y "%%F" "..\.." > nul
    )
)

:: Обновляем папки
for /f "delims=" %%D in ('dir /b /ad') do (
    if not "%%D"=="venv" (
        if exist "..\..\%%D" (
            xcopy /s /y /d "%%D" "..\..\%%D" > nul
        ) else (
            echo Добавление папки: %%D
            xcopy /s /y "%%D" "..\..\%%D" > nul
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