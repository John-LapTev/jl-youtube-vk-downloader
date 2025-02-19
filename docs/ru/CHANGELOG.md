# История изменений

## [1.3.1] - 2025-01-08

### Исправлено
- Исправлена проблема с загрузкой MP4 форматов
- Исправлен выбор форматов видео при скачивании
- Исправлена сборка программы в exe файл
- Исправлено некорректное отображение форматов в интерфейсе

### Технические улучшения
- Улучшена обработка аудио форматов для разных типов видео
- Оптимизирован процесс объединения видео и аудио дорожек
- Улучшена совместимость с FFmpeg для MP4 форматов
- Исправлены проблемы с кодировкой при сборке exe файла

## [1.3.0] - 2025-01-08

### Добавлено
- Поддержка языковых версий для YouTube видео
- Выбор языка при скачивании (переключение между доступными версиями)
- Автоматическое определение доступных языков видео
- Скачивание видео с сохранением названия на выбранном языке

### Улучшено
- Улучшено определение языков видео
- Оптимизирован список языков в интерфейсе
- Улучшена сортировка языков (русский и английский в начале списка)
- Добавлена расширенная поддержка языков

### Исправлено
- Исправлено определение аудиодорожек YouTube
- Исправлено отображение доступных языков
- Исправлена работа с метаданными на разных языках

## [1.2.0] - 2025-01-08

### Добавлено
- Поддержка скачивания видео из ВКонтакте
- Прямая поддержка vk.com ссылок
- Автоматическое определение форматов VK видео
- Поддержка видео с vkvideo.ru и других доменов VK

### Улучшено
- Улучшена обработка ошибок при скачивании
- Обновлено название программы на "JL YouTube & VK Video Downloader"
- Добавлена поддержка русского языка в заголовках запросов
- Улучшена обработка различных форматов видео

### Технические особенности
- Добавлены специальные настройки для VK API
- Улучшена обработка SSL-сертификатов
- Добавлена дополнительная обработка ошибок форматов
- Улучшена стабильность при работе с разными источниками видео

## [1.1.0] - 2025-01-08

### Добавлено
- Поддержка списков видео для массовой загрузки
- Загрузка плейлистов YouTube
- Автоматическое открытие папки после загрузки
- Сохранение списков URL в файл
- Загрузка списков URL из файла
- Автоматическое обновление yt-dlp при установке

### Улучшено
- Улучшена обработка SSL-сертификатов
- Улучшена стабильность загрузок
- Обновлен интерфейс программы
- Добавлена возможность очистки списка URL
- Улучшена обработка ошибок
- Улучшено логирование операций

### Технические особенности
- Python 3.10
- yt-dlp 2024.3.10
- customtkinter 5.2.1
- ffmpeg последней версии

### Исправлено
- Исправлены проблемы с сертификатами SSL
- Исправлены ошибки при загрузке плейлистов
- Исправлена работа с длинными списками URL

## [1.0.0] - 2025-01-07

### Добавлено
- Первый релиз программы
- Скачивание видео в разных разрешениях
- Конвертация в MP3
- Графический интерфейс на CustomTkinter
- Отображение прогресса загрузки
- Встроенный ffmpeg в exe-версии
- Поддержка запуска из исходного кода

### Технические особенности
- Python 3.10
- yt-dlp 2024.12.23
- customtkinter 5.2.2
- ffmpeg последней версии

### Известные проблемы
- Нет автоматического обновления
- Требуется обновление программы при изменении защиты YouTube