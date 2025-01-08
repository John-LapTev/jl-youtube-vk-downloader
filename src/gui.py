import customtkinter as ctk
from downloader import YouTubeDownloader
import threading
import webbrowser
from tkinter import filedialog
import os
from datetime import timedelta
import logging

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title("JL YouTube & VK Video Downloader")
        self.geometry("500x700")  # Увеличенная высота для новых элементов
        self.minsize(500, 700)
        
        # Настройка темы и цветов
        self.colors = {
            "bg": "#1E1E1E",
            "card": "#252526",
            "button": "#2D5A88",
            "button_hover": "#3A75B0",
            "accent": "#61AFEF"
        }
        
        self.configure(fg_color=self.colors["bg"])
        ctk.set_appearance_mode("dark")
        
        # Инициализация
        self.downloader = YouTubeDownloader()
        self.current_formats = []
        self.current_audio_tracks = []  # Список доступных аудиодорожек
        self.output_path = os.path.expanduser("~/Downloads")
        
        # UI
        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса"""
        # Основной контейнер
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Секция режима работы
        mode_section = ctk.CTkFrame(container, fg_color=self.colors["card"], corner_radius=10)
        mode_section.pack(fill="x", padx=5, pady=5)
        
        self.mode_var = ctk.StringVar(value="single")
        modes = [
            ("single", "Одно видео"),
            ("multiple", "Список видео"),
            ("playlist", "Плейлист")
        ]
        
        mode_frame = ctk.CTkFrame(mode_section, fg_color="transparent")
        mode_frame.pack(fill="x", padx=15, pady=10)
        
        for mode, text in modes:
            rb = ctk.CTkRadioButton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=mode,
                command=self.on_mode_change
            )
            rb.pack(side="left", padx=10)
        
        # Секция URL
        url_section = ctk.CTkFrame(container, fg_color=self.colors["card"], corner_radius=10)
        url_section.pack(fill="x", padx=5, pady=5)
        
        # Фрейм для одного URL
        self.single_url_frame = ctk.CTkFrame(url_section, fg_color="transparent")
        
        # Поле ввода URL
        self.url_entry = ctk.CTkEntry(
            self.single_url_frame,
            placeholder_text="Вставьте ссылку на видео",
            height=40,
            font=("Arial", 12)
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=15, pady=15)
        
        # Кнопка вставки
        paste_button = ctk.CTkButton(
            self.single_url_frame,
            text="📋",
            width=40,
            height=40,
            command=self.paste_from_clipboard
        )
        paste_button.pack(side="right", padx=(0, 15))
        
        # Фрейм для множественных URL
        self.multiple_url_frame = ctk.CTkFrame(url_section, fg_color="transparent")
        
        # Кнопки управления списком URL
        urls_buttons = ctk.CTkFrame(self.multiple_url_frame, fg_color="transparent")
        urls_buttons.pack(fill="x", padx=15, pady=(15,5))
        
        ctk.CTkButton(
            urls_buttons,
            text="Загрузить из файла",
            width=150,
            command=self.load_urls_from_file
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            urls_buttons,
            text="Сохранить в файл",
            width=150,
            command=self.save_urls_to_file
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            urls_buttons,
            text="Очистить",
            width=100,
            command=self.clear_urls
        ).pack(side="left", padx=5)
        
        # Текстовое поле для списка URL
        self.urls_text = ctk.CTkTextbox(
            self.multiple_url_frame,
            height=100,
            font=("Arial", 12)
        )
        self.urls_text.pack(fill="x", padx=15, pady=(5,15))
        
        # Изначально показываем фрейм для одного URL
        self.single_url_frame.pack(fill="x")
        
        # Секция информации
        info_section = ctk.CTkFrame(container, fg_color=self.colors["card"], corner_radius=10)
        info_section.pack(fill="x", padx=5, pady=5)
        
        self.title_label = ctk.CTkLabel(
            info_section,
            text="",
            wraplength=440,
            anchor="w",
            justify="left",
            font=("Arial", 12)
        )
        self.title_label.pack(fill="x", padx=15, pady=(15, 0))
        
        self.duration_label = ctk.CTkLabel(
            info_section,
            text="",
            anchor="w",
            font=("Arial", 12)
        )
        self.duration_label.pack(fill="x", padx=15, pady=(5, 15))
        
        # Кнопка получения информации
        self.info_button = ctk.CTkButton(
            info_section,
            text="Получить информацию",
            height=40,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            command=self.get_video_info
        )
        self.info_button.pack(fill="x", padx=15, pady=(0, 15))
        
        # Секция настроек загрузки
        settings_section = ctk.CTkFrame(container, fg_color=self.colors["card"], corner_radius=10)
        settings_section.pack(fill="x", padx=5, pady=5)
        
        # Выбор формата видео
        self.format_var = ctk.StringVar(value="")
        self.format_menu = ctk.CTkOptionMenu(
            settings_section,
            variable=self.format_var,
            values=[""],
            width=200,
            height=40,
            state="disabled",
            font=("Arial", 12)
        )
        self.format_menu.pack(fill="x", padx=15, pady=15)
        
        # Выбор аудиодорожки
        self.audio_var = ctk.StringVar(value="")
        self.audio_menu = ctk.CTkOptionMenu(
            settings_section,
            variable=self.audio_var,
            values=[""],
            width=200,
            height=40,
            state="disabled",
            font=("Arial", 12)
        )
        self.audio_menu.pack(fill="x", padx=15, pady=(0, 15))
        
        # Автооткрытие папки
        self.auto_open_var = ctk.BooleanVar(value=self.downloader.settings.get('auto_open_folder', False))
        auto_open_cb = ctk.CTkCheckBox(
            settings_section,
            text="Открывать папку после загрузки",
            variable=self.auto_open_var,
            command=self.save_settings
        )
        auto_open_cb.pack(padx=15, pady=(0, 15))
        
        # Выбор папки сохранения
        path_frame = ctk.CTkFrame(settings_section, fg_color="transparent")
        path_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.path_label = ctk.CTkLabel(
            path_frame,
            text=f"📁 {self.output_path}",
            anchor="w",
            font=("Arial", 12)
        )
        self.path_label.pack(side="left", fill="x", expand=True)
        
        self.open_folder_button = ctk.CTkButton(
            path_frame,
            text="📂",
            width=40,
            height=30,
            command=self.open_output_folder
        )
        self.open_folder_button.pack(side="left", padx=(0, 5))
        
        self.path_button = ctk.CTkButton(
            path_frame,
            text="Изменить",
            width=100,
            height=30,
            command=self.choose_directory
        )
        self.path_button.pack(side="right")
        
        # Кнопки загрузки
        buttons_frame = ctk.CTkFrame(settings_section, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.video_button = ctk.CTkButton(
            buttons_frame,
            text="Скачать видео",
            height=40,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            state="disabled",
            command=self.start_video_download
        )
        self.video_button.pack(side="left", expand=True, padx=(0, 5))
        
        self.audio_button = ctk.CTkButton(
            buttons_frame,
            text="Скачать MP3",
            height=40,
            fg_color=self.colors["button"],
            hover_color=self.colors["button_hover"],
            state="disabled",
            command=self.start_audio_download
        )
        self.audio_button.pack(side="right", expand=True, padx=(5, 0))
        
        # Секция прогресса
        progress_section = ctk.CTkFrame(container, fg_color=self.colors["card"], corner_radius=10)
        progress_section.pack(fill="x", padx=5, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_section,
            height=6,
            corner_radius=3,
            progress_color=self.colors["accent"]
        )
        self.progress_bar.pack(fill="x", padx=15, pady=(15, 0))
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(
            progress_section,
            text="",
            font=("Arial", 12)
        )
        self.progress_label.pack(pady=15)
        
        # Футер
        footer = ctk.CTkFrame(container, fg_color="transparent")
        footer.pack(fill="x", pady=(5, 0))
        
        telegram_button = ctk.CTkButton(
            footer,
            text="Telegram Channel",
            width=150,
            height=35,
            command=lambda: webbrowser.open('https://t.me/JL_Stable_Diffusion')
        )
        telegram_button.pack(side="right")

    def on_mode_change(self):
        """Обработчик смены режима работы"""
        mode = self.mode_var.get()
        
        # Скрываем оба фрейма
        self.single_url_frame.pack_forget()
        self.multiple_url_frame.pack_forget()
        
        # Показываем нужный фрейм
        if mode == "single":
            self.single_url_frame.pack(fill="x")
            self.clear_urls()
        else:
            self.multiple_url_frame.pack(fill="x")
            self.url_entry.delete(0, "end")

    def save_settings(self):
        """Сохранение настроек"""
        self.downloader.save_settings({
            'auto_open_folder': self.auto_open_var.get()
        })

    def get_urls_list(self) -> list:
        """Получение списка URL в зависимости от режима"""
        mode = self.mode_var.get()
        
        if mode == "single":
            url = self.url_entry.get().strip()
            return [url] if url else []
            
        elif mode == "playlist":
            url = self.urls_text.get("1.0", "end").strip()
            if url:
                try:
                    return [video['url'] for video in self.downloader.get_playlist_videos(url)]
                except Exception as e:
                    self.show_error(f"Ошибка получения плейлиста: {str(e)}")
                    return []
        else:
            # Режим множественной загрузки
            urls = self.urls_text.get("1.0", "end").strip().split('\n')
            return [url.strip() for url in urls if url.strip()]

    def get_video_info(self):
        """Получение информации о видео"""
        urls = self.get_urls_list()
        if not urls:
            self.progress_label.configure(text="❌ Введите URL!")
            return
        
        def info_thread():
            try:
                self.disable_controls()
                self.progress_label.configure(text="⏳ Получение информации...")
                self.progress_bar.set(0)
                
                # Получаем информацию о первом видео для определения форматов
                info = self.downloader.get_video_info(urls[0])
                
                if len(urls) == 1:
                    duration = str(timedelta(seconds=info['duration']))
                    self.title_label.configure(text=info['title'])
                    self.duration_label.configure(text=f"⏱️ Длительность: {duration}")
                else:
                    self.title_label.configure(text=f"Выбрано видео: {len(urls)}")
                    self.duration_label.configure(text="")
                
                # Обновляем форматы видео
                self.current_formats = info['formats']
                format_strings = []
                for f in self.current_formats:
                    size_str = self.format_size(f['filesize']) if f['filesize'] else 'N/A'
                    format_strings.append(f"{f['resolution']} - {size_str} ({f['ext']})")
                
                self.format_menu.configure(values=format_strings, state="normal")
                if format_strings:
                    self.format_var.set(format_strings[0])
                
                # Обновляем аудиодорожки
                self.current_audio_tracks = info.get('audio_tracks', [])
                if len(self.current_audio_tracks) > 1:  # Если есть выбор аудиодорожек
                    audio_options = [
                        f"{track['language_name']}"
                        for track in self.current_audio_tracks
                    ]
                    self.audio_menu.configure(values=audio_options, state="normal")
                    self.audio_var.set(audio_options[0])
                else:
                    self.audio_menu.configure(values=["Аудио по умолчанию"], state="disabled")
                    self.audio_var.set("Аудио по умолчанию")
                
                # Активируем кнопки
                self.video_button.configure(state="normal")
                self.audio_button.configure(state="normal")
                
                self.progress_label.configure(text="✅ Информация получена!")
                
            except Exception as e:
                self.show_error(str(e))
            finally:
                self.enable_controls()
        
        thread = threading.Thread(target=info_thread)
        thread.daemon = True
        thread.start()

    def format_size(self, size_bytes):
        """Форматирование размера файла"""
        if not size_bytes:
            return 'N/A'
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

    def start_video_download(self):
        """Запуск загрузки видео"""
        def download_thread():
            urls = self.get_urls_list()
            if not urls:
                self.progress_label.configure(text="❌ Введите URL!")
                return

            try:
                self.disable_controls()
                self.progress_bar.set(0)

                # Получаем выбранный формат
                selected_format_str = self.format_var.get()
                selected_format = None
                for fmt in self.current_formats:
                    # Проверяем и разрешение, и формат файла
                    format_str = f"{fmt['resolution']} - {self.format_size(fmt['filesize'])} ({fmt['ext']})"
                    if format_str == selected_format_str:
                        selected_format = fmt
                        break

                if not selected_format:
                    raise Exception("Формат не найден")

                # Получаем выбранную аудиодорожку
                selected_audio = None
                selected_audio_name = self.audio_var.get()
                if selected_audio_name != "Аудио по умолчанию":
                    for track in self.current_audio_tracks:
                        if track['language_name'] == selected_audio_name:
                            selected_audio = track['language']
                            break

                # Загружаем каждое видео
                total_videos = len(urls)
                for i, url in enumerate(urls, 1):
                    self.progress_label.configure(text=f"⏳ Загрузка видео {i} из {total_videos}...")
                    
                    self.downloader.download_video(
                        url,
                        selected_format['format_id'],
                        self.output_path,
                        audio_lang=selected_audio,
                        progress_callback=lambda p, d, t: self.update_progress(p, d, t, i, total_videos),
                        completion_callback=lambda: self.on_video_complete(i, total_videos)
                    )

                self.progress_label.configure(text="✅ Все загрузки завершены!")
                
                # Открываем папку если включено
                if self.downloader.settings.get('auto_open_folder', False):
                    self.open_output_folder()

            except Exception as e:
                self.show_error(str(e))
            finally:
                self.enable_controls()

        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()

    def start_audio_download(self):
        """Запуск загрузки аудио"""
        def download_thread():
            urls = self.get_urls_list()
            if not urls:
                self.progress_label.configure(text="❌ Введите URL!")
                return

            try:
                self.disable_controls()
                self.progress_bar.set(0)

                # Получаем выбранную аудиодорожку
                selected_audio = None
                selected_audio_name = self.audio_var.get()
                if selected_audio_name != "Аудио по умолчанию":
                    for track in self.current_audio_tracks:
                        if track['language_name'] == selected_audio_name:
                            selected_audio = track['language']
                            break

                # Загружаем каждое аудио
                total_videos = len(urls)
                for i, url in enumerate(urls, 1):
                    self.progress_label.configure(text=f"⏳ Загрузка аудио {i} из {total_videos}...")
                    
                    self.downloader.download_audio(
                        url,
                        self.output_path,
                        audio_lang=selected_audio,
                        progress_callback=lambda p, d, t: self.update_progress(p, d, t, i, total_videos),
                        completion_callback=lambda: self.on_video_complete(i, total_videos)
                    )

                self.progress_label.configure(text="✅ Все загрузки завершены!")
                
                # Открываем папку если включено
                if self.downloader.settings.get('auto_open_folder', False):
                    self.open_output_folder()

            except Exception as e:
                self.show_error(str(e))
            finally:
                self.enable_controls()

        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()

    def update_progress(self, progress: float, downloaded: int, total: int,
                       current_num: int = 1, total_num: int = 1):
        """Обновление прогресса загрузки"""
        self.progress_bar.set(progress / 100)
        
        # Форматируем размеры
        downloaded_str = self.format_size(downloaded)
        total_str = self.format_size(total)
        
        # Обновляем текст прогресса
        if total_num > 1:
            self.progress_label.configure(
                text=f"⬇️ Файл {current_num} из {total_num}: "
                     f"{downloaded_str} из {total_str} ({progress:.1f}%)"
            )
        else:
            self.progress_label.configure(
                text=f"⬇️ Загружено: {downloaded_str} из {total_str} ({progress:.1f}%)"
            )
        
        self.update_idletasks()

    def disable_controls(self):
        """Отключение элементов управления"""
        self.info_button.configure(state="disabled")
        self.video_button.configure(state="disabled")
        self.audio_button.configure(state="disabled")
        self.format_menu.configure(state="disabled")
        self.audio_menu.configure(state="disabled")  # Отключаем меню аудио
        self.path_button.configure(state="disabled")

    def enable_controls(self):
        """Включение элементов управления"""
        self.info_button.configure(state="normal")
        self.video_button.configure(state="normal")
        self.audio_button.configure(state="normal")
        self.format_menu.configure(state="normal")
        if len(self.current_audio_tracks) > 1:  # Включаем меню аудио только если есть выбор
            self.audio_menu.configure(state="normal")
        self.path_button.configure(state="normal")

    def on_video_complete(self, current: int, total: int):
        """Обработчик завершения загрузки одного файла"""
        self.progress_label.configure(text=f"✅ Загружено {current} из {total}")
        self.progress_bar.set(current / total)

    def paste_from_clipboard(self):
        """Вставка из буфера обмена"""
        try:
            clipboard_text = self.clipboard_get()
            if self.mode_var.get() == "single":
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, clipboard_text)
            else:
                self.urls_text.insert("end", clipboard_text + "\n")
        except Exception:
            pass

    def choose_directory(self):
        """Выбор папки для сохранения"""
        dir_path = filedialog.askdirectory(initialdir=self.output_path)
        if dir_path:
            self.output_path = dir_path
            self.path_label.configure(text=f"📁 {self.output_path}")

    def open_output_folder(self):
        """Открытие папки с загрузками"""
        try:
            os.startfile(self.output_path)
        except Exception as e:
            self.progress_label.configure(text=f"❌ Ошибка открытия папки: {str(e)}")

    def load_urls_from_file(self):
        """Загрузка списка URL из файла"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = f.read()
                self.urls_text.delete("1.0", "end")
                self.urls_text.insert("1.0", urls)
            except Exception as e:
                self.show_error(f"Ошибка загрузки файла: {str(e)}")

    def save_urls_to_file(self):
        """Сохранение списка URL в файл"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                urls = self.urls_text.get("1.0", "end").strip()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(urls)
            except Exception as e:
                self.show_error(f"Ошибка сохранения файла: {str(e)}")

    def clear_urls(self):
        """Очистка списка URL"""
        if self.mode_var.get() == "single":
            self.url_entry.delete(0, "end")
        else:
            self.urls_text.delete("1.0", "end")

    def show_error(self, message: str):
        """Показ сообщения об ошибке"""
        logging.error(message)
        self.progress_label.configure(text=f"❌ {message}")
        self.progress_bar.set(0)