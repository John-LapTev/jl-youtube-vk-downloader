# Change Log

## [1.3.1] - 2025-01-08

### Fixed
- Fixed MP4 format downloading issues
- Fixed video format selection during download
- Fixed program build to exe file
- Fixed format display in interface

### Technical Improvements
- Improved audio format handling for different video types
- Optimized video and audio track merging process
- Improved FFmpeg compatibility for MP4 formats
- Fixed encoding issues during exe file build

## [1.3.0] - 2025-01-08

### Added
- Language version support for YouTube videos
- Language selection when downloading
- Automatic language detection for videos
- Save videos with titles in selected language

### Improved
- Enhanced video language detection
- Optimized language list in interface
- Improved language sorting (Russian and English at the top)
- Added extended language support

### Fixed
- Fixed YouTube audio track detection
- Fixed available languages display
- Fixed metadata handling in different languages

## [1.2.0] - 2025-01-08

### Added
- VK video download support
- Direct vk.com link support
- Automatic VK video format detection
- Support for vkvideo.ru and other VK domains

### Improved
- Enhanced download error handling
- Updated program name to "JL YouTube & VK Video Downloader"
- Added Russian language support in request headers
- Improved handling of various video formats

### Technical Details
- Added special settings for VK API
- Improved SSL certificate handling
- Added additional format error handling
- Improved stability when working with different video sources

## [1.1.0] - 2025-01-08

### Added
- Support for video lists for bulk downloads
- YouTube playlist downloads
- Auto-open folder after download
- Save URL lists to file
- Load URL lists from file
- Automatic yt-dlp updates during installation

### Improved
- Improved SSL certificate handling
- Improved download stability
- Updated program interface
- Added URL list clearing capability
- Improved error handling
- Improved operation logging

### Technical Details
- Python 3.10
- yt-dlp 2024.3.10
- customtkinter 5.2.1
- Latest version of ffmpeg

### Fixed
- Fixed SSL certificate issues
- Fixed playlist downloading errors
- Fixed long URL list handling

## [1.0.0] - 2025-01-07

### Added
- First program release
- Video downloading in different resolutions
- MP3 conversion
- CustomTkinter graphical interface
- Download progress display
- Built-in ffmpeg in exe version
- Support for running from source code

### Technical Details
- Python 3.10
- yt-dlp 2024.12.23
- customtkinter 5.2.2
- Latest version of ffmpeg

### Known Issues
- No automatic updates
- Program update required when YouTube protection changes