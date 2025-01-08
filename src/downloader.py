import yt_dlp
from typing import Callable, Optional, List, Dict
import logging
import os
import sys
import json
from pathlib import Path
import ssl

# Отключаем проверку SSL на уровне Python
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Настраиваем логирование
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('downloader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class YouTubeDownloader:
    def __init__(self):
        # Создаём папки для настроек
        self.config_dir = Path.home() / '.jl_youtube_downloader'
        self.config_dir.mkdir(exist_ok=True)
        self.settings_path = self.config_dir / 'settings.json'
        self.current_formats = []
        
        # Загружаем настройки
        self.settings = self._load_settings()
        
        # Настраиваем базовые параметры
        self.base_opts = {
            'quiet': False,
            'no_warnings': False,
            'format_sort': ['res', 'ext'],
            'ffmpeg_location': self._get_ffmpeg_path(),
            
            # Параметры SSL и безопасности
            'nocheckcertificate': True,
            'no_check_certificates': True,
            'legacy_server_connect': True,
            
            # Таймауты и повторы
            'socket_timeout': 30,
            'retries': 10,
            'file_access_retries': 10,
            
            # Обновленные заголовки
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
            },
            
            # Параметры для экстракторов видео
            'extractor_args': {
                'youtube': {
                    'player_skip': ['configs', 'webpage'],
                    'skip': ['hls', 'dash', 'translated_tabs'],
                },
                'vk': {
                    'direct_links': True,
                    'force_direct_links': True,
                    'use_direct_dl': True,
                }
            },
            
            # Дополнительные параметры
            'extract_flat': False,
            'force_generic_extractor': False,
            'geo_bypass': True,
            'geo_bypass_country': 'RU',
        }

    def format_size(self, size_bytes):
        """Форматирование размера файла"""
        if not size_bytes:
            return 'N/A'
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

    def _get_ffmpeg_path(self) -> str:
        """Получение пути к ffmpeg"""
        if getattr(sys, 'frozen', False):
            import tempfile
            temp_dir = tempfile._get_default_tempdir()
            ffmpeg_path = os.path.join(temp_dir, 'ffmpeg.exe')
            if not os.path.exists(ffmpeg_path):
                with open(os.path.join(sys._MEIPASS, 'ffmpeg.exe'), 'rb') as f_src:
                    with open(ffmpeg_path, 'wb') as f_dst:
                        f_dst.write(f_src.read())
            return ffmpeg_path
        else:
            return 'ffmpeg.exe'

    def _load_settings(self) -> dict:
        """Загрузка настроек из файла"""
        try:
            if self.settings_path.exists():
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Ошибка загрузки настроек: {e}")
        return {'auto_open_folder': False}

    def save_settings(self, settings: dict):
        """Сохранение настроек в файл"""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f)
            self.settings = settings
        except Exception as e:
            logging.error(f"Ошибка сохранения настроек: {e}")

    def get_video_info(self, url: str) -> dict:
        """Получает информацию о видео"""
        ydl_opts = {
            **self.base_opts,
            'format': 'bestvideo*+bestaudio/best',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if info is None:
                    raise Exception("Не удалось получить информацию о видео")
                    
                formats = self._extract_formats(info['formats'])
                audio_tracks = self._extract_audio_tracks(info['formats'], info)
                
                # Сохраняем форматы для последующего использования
                self.current_formats = formats
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'formats': formats,
                    'audio_tracks': audio_tracks
                }
            except Exception as e:
                logging.error(f"Ошибка получения информации о видео: {str(e)}")
                raise Exception(f"Ошибка получения информации: {str(e)}")

    def _extract_formats(self, formats: list) -> list:
        """Извлекает форматы видео и их размеры"""
        video_formats = []
        seen_resolutions = {}
        
        for f in formats:
            try:
                # Пропускаем неподходящие форматы
                if not f or not f.get('height') or f.get('vcodec') == 'none':
                    continue
                    
                height = f.get('height')
                ext = f.get('ext', 'unknown')
                filesize = f.get('filesize') or f.get('filesize_approx', 0)
                format_id = f.get('format_id', 'unknown')
                resolution = f"{height}p"
                
                format_info = {
                    'format_id': format_id,
                    'resolution': resolution,
                    'ext': ext,
                    'filesize': filesize,
                    'vcodec': f.get('vcodec', ''),
                    'acodec': f.get('acodec', '')
                }
                
                # Ключ, учитывающий и разрешение, и формат
                key = f"{resolution}_{ext}"
                
                # Сохраняем формат с лучшим качеством для каждой комбинации разрешения и расширения
                if key not in seen_resolutions or filesize > seen_resolutions[key]['filesize']:
                    seen_resolutions[key] = format_info
                    
            except Exception as e:
                logging.warning(f"Ошибка обработки формата {f.get('format_id')}: {str(e)}")
                continue

        video_formats = list(seen_resolutions.values())
        
        # Если форматы не найдены, добавляем базовый
        if not video_formats:
            video_formats.append({
                'format_id': 'best',
                'resolution': 'auto',
                'ext': 'mp4',
                'filesize': 0,
                'vcodec': 'unknown',
                'acodec': 'unknown'
            })
        
        # Сортируем сначала по разрешению, потом по расширению
        def sort_key(fmt):
            res = int(fmt['resolution'].replace('p', '')) if fmt['resolution'] != 'auto' else 0
            return (-res, fmt['ext'])  # Сортировка по убыванию разрешения, потом по расширению
            
        video_formats.sort(key=sort_key)
        
        logging.debug("=== Доступные форматы видео ===")
        for fmt in video_formats:
            size_str = self.format_size(fmt['filesize'])
            logging.debug(f"Формат: {fmt['resolution']} - {size_str} ({fmt['ext']}) [ID: {fmt['format_id']}]")
        
        return video_formats

    def _extract_audio_tracks(self, formats: list, info: dict = None) -> list:
        """Извлекает информацию о доступных аудиодорожках и языковых версиях"""
        audio_tracks = []
        seen_langs = set()
        
        try:
            # Выводим в лог всю информацию о языках для отладки
            if info:
                logging.debug("=== Информация о языках видео ===")
                logging.debug(f"Языки в info: {info.get('languages', [])}")
                logging.debug(f"Субтитры: {list(info.get('subtitles', {}).keys())}")
                logging.debug(f"Форматы с аудио: {[(f.get('format_id'), f.get('language'), f.get('acodec')) for f in formats if f.get('acodec') != 'none']}")

            # Добавляем языки из субтитров как доступные языковые версии
            if info and 'subtitles' in info:
                for lang_code in info['subtitles'].keys():
                    # Пропускаем технические поля
                    if lang_code == 'live_chat':
                        continue
                    
                    # Пропускаем уже добавленные языки
                    if lang_code in seen_langs:
                        continue
                    
                    seen_langs.add(lang_code)
                    track = {
                        'format_id': 'bestaudio',  # Будем использовать лучшее качество аудио
                        'language': lang_code,
                        'language_name': self._get_language_name(lang_code),
                        'acodec': 'opus',  # Обычно YouTube использует opus для аудио
                        'filesize': 0,
                        'is_original': False
                    }
                    audio_tracks.append(track)

            # Добавляем оригинальную версию, если она отличается от уже добавленных
            original_lang = next((f.get('language') for f in formats if f.get('acodec') != 'none'), None)
            if original_lang and original_lang not in seen_langs:
                track = {
                    'format_id': 'bestaudio',
                    'language': original_lang,
                    'language_name': self._get_language_name(original_lang),
                    'acodec': next((f.get('acodec') for f in formats if f.get('acodec') != 'none'), 'unknown'),
                    'filesize': 0,
                    'is_original': True
                }
                audio_tracks.append(track)
                seen_langs.add(original_lang)

            # Если не нашли ни одного языка, добавляем оригинальную версию
            if not audio_tracks:
                audio_tracks.append({
                    'format_id': 'bestaudio',
                    'language': 'original',
                    'language_name': 'Оригинальная версия',
                    'acodec': 'unknown',
                    'filesize': 0,
                    'is_original': True
                })

            # Сортируем: сначала русский, потом английский, потом остальные
            def sort_key(track):
                lang = track['language']
                if lang == 'ru':
                    return (0, track['language_name'])
                elif lang == 'en':
                    return (1, track['language_name'])
                elif track['is_original']:
                    return (999, track['language_name'])
                else:
                    return (2, track['language_name'])

            audio_tracks.sort(key=sort_key)

            # Выводим в лог найденные аудиодорожки
            logging.debug("=== Найденные аудиодорожки ===")
            for track in audio_tracks:
                logging.debug(f"Аудиодорожка: {track['language_name']} ({track['language']})")
            
        except Exception as e:
            logging.error(f"Ошибка при извлечении аудиодорожек: {str(e)}")
            # В случае ошибки возвращаем оригинальную дорожку
            audio_tracks = [{
                'format_id': 'bestaudio',
                'language': 'original',
                'language_name': 'Оригинальная версия',
                'acodec': 'unknown',
                'filesize': 0,
                'is_original': True
            }]
        
        return audio_tracks

    def _get_language_name(self, lang_code: str) -> str:
        """Возвращает название языка по коду"""
        if lang_code == 'original':
            return 'Оригинальная версия'
            
        language_names = {
            'ru': 'Русский',
            'en': 'Английский',
            'fr': 'Французский',
            'de': 'Немецкий',
            'es': 'Испанский',
            'it': 'Итальянский',
            'ja': 'Японский',
            'ko': 'Корейский',
            'zh': 'Китайский',
            'ar': 'Арабский',
            'hi': 'Хинди',
            'pt': 'Португальский',
            'nl': 'Голландский',
            'pl': 'Польский',
            'tr': 'Турецкий',
            'vi': 'Вьетнамский',
            'th': 'Тайский',
            'cs': 'Чешский',
            'el': 'Греческий',
            'hu': 'Венгерский',
            'ro': 'Румынский',
            'default': 'По умолчанию'
        }
        return language_names.get(lang_code.lower(), f'Язык: {lang_code}')

    def download_video(self, url: str, format_id: str, output_path: str,
                      audio_lang: str = None,
                      progress_callback: Optional[Callable] = None,
                      completion_callback: Optional[Callable] = None) -> None:
        """Загружает видео"""
        # Получаем выбранный формат
        selected_format = next((f for f in self.current_formats if f['format_id'] == format_id), None)
        if not selected_format:
            raise Exception("Формат не найден")

        # Определяем формат аудио в зависимости от формата видео
        if selected_format['ext'] == 'webm':
            audio_format = 'bestaudio[ext=webm]'
        else:
            audio_format = 'bestaudio[ext=m4a]'

        # Если указан язык, добавляем его в параметры
        if audio_lang and audio_lang != 'original':
            audio_format = f'{audio_format}[language={audio_lang}]'

        # Формируем строку формата
        format_spec = f'{format_id}+{audio_format}/bestaudio'

        ydl_opts = {
            **self.base_opts,
            'format': format_spec,
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'merge_output_format': selected_format['ext'],
            'postprocessor_args': [
                '-c:v', 'copy',
                '-c:a', 'copy'
            ],
            'overwrites': True,
        }

        # Добавляем параметры для языка
        if audio_lang and audio_lang != 'original':
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_skip': ['configs', 'webpage'],
                    'skip': ['hls', 'dash', 'translated_tabs'],
                    'lang': [audio_lang]
                }
            }

        def progress_hook(d):
            """Обработчик прогресса загрузки"""
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0)
                if not total:
                    total = d.get('total_bytes_estimate', 0)
                
                if total > 0 and progress_callback:
                    progress = (downloaded / total) * 100
                    progress_callback(progress, downloaded, total)
                    
            elif d['status'] == 'finished':
                if completion_callback:
                    completion_callback()
            
            elif d['status'] == 'error':
                logging.error(f"Ошибка загрузки: {d.get('error')}")

        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Получаем информацию о файле
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                
                # Удаляем существующий файл если есть
                if os.path.exists(filename):
                    os.remove(filename)
                    logging.info(f"Удалён существующий файл: {filename}")
                
                # Скачиваем файл
                error_code = ydl.download([url])
                if error_code != 0:
                    raise Exception(f"yt-dlp вернул код ошибки: {error_code}")
                
        except Exception as e:
            logging.error(f"Ошибка загрузки: {str(e)}")
            raise Exception(f"Ошибка загрузки: {str(e)}")

    def download_audio(self, url: str, output_path: str,
                    audio_lang: str = None,
                    progress_callback: Optional[Callable] = None,
                    completion_callback: Optional[Callable] = None) -> None:
        """Загружает аудио в MP3"""
        format_spec = 'bestaudio'
        if audio_lang and audio_lang != 'original':
            format_spec = f'bestaudio[language={audio_lang}]/bestaudio'
            
        ydl_opts = {
            **self.base_opts,
            'format': format_spec,
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'overwrites': True,
        }

        # Добавляем выбор языка, если он указан
        if audio_lang and audio_lang != 'original':
            ydl_opts['extractor_args'] = {
                'youtube': {
                    'player_skip': ['configs', 'webpage'],
                    'skip': ['hls', 'dash', 'translated_tabs'],
                    'lang': [audio_lang]
                }
            }

        def progress_hook(d):
            """Обработчик прогресса загрузки аудио"""
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', 0)
                if not total:
                    total = d.get('total_bytes_estimate', 0)
                
                if total > 0 and progress_callback:
                    progress = (downloaded / total) * 100
                    progress_callback(progress, downloaded, total)
                    
            elif d['status'] == 'finished':
                if completion_callback:
                    completion_callback()

        ydl_opts['progress_hooks'] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Получаем информацию о файле
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                filename_mp3 = os.path.splitext(filename)[0] + '.mp3'
                
                # Удаляем существующий файл если есть
                if os.path.exists(filename_mp3):
                    os.remove(filename_mp3)
                    logging.info(f"Удалён существующий файл: {filename_mp3}")
                
                # Скачиваем и конвертируем в MP3
                error_code = ydl.download([url])
                if error_code != 0:
                    raise Exception(f"yt-dlp вернул код ошибки: {error_code}")
                
        except Exception as e:
            logging.error(f"Ошибка загрузки аудио: {str(e)}")
            raise Exception(f"Ошибка загрузки аудио: {str(e)}")

    def get_playlist_videos(self, url: str) -> List[Dict]:
        """Получает список всех видео из плейлиста"""
        try:
            with yt_dlp.YoutubeDL({**self.base_opts, 'extract_flat': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    return [
                        {
                            'url': entry.get('url', entry.get('webpage_url', '')),
                            'title': entry.get('title', 'Unknown'),
                            'duration': entry.get('duration', 0)
                        }
                        for entry in info['entries']
                        if entry is not None
                    ]
                raise Exception("Это не плейлист")
        except Exception as e:
            logging.error(f"Ошибка получения информации о плейлисте: {e}")
            raise