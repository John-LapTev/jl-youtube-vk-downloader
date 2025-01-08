import sys
import traceback
import tkinter as tk
from tkinter import messagebox
from gui import App
import logging
from pathlib import Path

# Версия приложения
APP_VERSION = "1.3.1"

def setup_logging():
    """Настройка системы логирования"""
    # Создаем папку для логов если её нет
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Настраиваем формат логирования
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            # Логирование в файл
            logging.FileHandler(
                log_dir / 'app.log',
                encoding='utf-8',
                mode='w'
            ),
            # Вывод в консоль
            logging.StreamHandler()
        ]
    )
    
    # Перехватываем необработанные исключения
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Стандартная обработка Ctrl+C
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logging.error("Необработанное исключение:", 
                     exc_info=(exc_type, exc_value, exc_traceback))
    
    sys.excepthook = handle_exception

def show_error(error_msg: str):
    """Показывает окно с ошибкой"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Ошибка",
            f"Произошла неожиданная ошибка:\n\n{error_msg}\n\n"
            "Подробности можно найти в файле logs/app.log"
        )
        root.destroy()
    except Exception as e:
        # Если не удалось показать окно, выводим в консоль
        print(f"Ошибка: {error_msg}")
        print(f"Не удалось показать окно ошибки: {e}")

def check_requirements():
    """Проверка наличия необходимых компонентов"""
    try:
        # Проверяем наличие ffmpeg при запуске из исходников
        if not getattr(sys, 'frozen', False):
            ffmpeg_path = Path('ffmpeg.exe')
            if not ffmpeg_path.exists():
                raise Exception(
                    "Не найден ffmpeg.exe. Пожалуйста, убедитесь что файл "
                    "ffmpeg.exe находится в папке с программой."
                )
        
        # Здесь можно добавить другие проверки
        # Например, наличие необходимых библиотек
        
    except Exception as e:
        logging.error(f"Ошибка при проверке требований: {e}")
        show_error(str(e))
        sys.exit(1)

def main():
    """Главная функция программы"""
    try:
        # Настраиваем логирование
        setup_logging()
        logging.info("Запуск программы")
        
        # Проверяем требования
        check_requirements()
        
        # Создаём и запускаем главное окно
        app = App()
        app.mainloop()
        
    except Exception as e:
        # Логируем ошибку
        logging.error("Критическая ошибка:", exc_info=True)
        
        # Формируем текст ошибки
        error_msg = f"{str(e)}\n\n"
        error_msg += traceback.format_exc()
        
        # Показываем ошибку пользователю
        show_error(error_msg)
        
        sys.exit(1)
        
    finally:
        logging.info("Завершение программы")

if __name__ == "__main__":
    main()