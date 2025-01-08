# User Guide

## Installation

### Portable Version (Recommended)
1. Download the latest version from [Releases](link_to_releases)
2. Extract the archive to any folder
3. Run the exe file
4. All downloads will be saved in the 'downloads' folder

### From Source Code
1. Install Python 3.10 or newer
2. Clone or download the repository
3. Run setup.bat to install dependencies
4. Use run.bat to start the program

Note: When running from source, ffmpeg.exe must be in the root folder. The setup.bat script will download it automatically.

## Usage

### Single Video Download
1. Select "Single Video" mode
2. Paste the video link
3. Click "Get Info"
4. Select video quality
5. Select language (if available)
6. Click "Download Video" or "Download MP3"

### Multiple Videos Download
1. Select "Multiple Videos" mode
2. Enter or paste links (one per line)
3. Click "Get Info"
4. Select format for all videos
5. Click "Download Video"

### Playlist Download
1. Select "Playlist" mode
2. Paste the playlist link
3. Click "Get Info"
4. Select quality for all videos
5. Click "Download Video"

## Supported Links

### YouTube
- Regular videos: youtube.com/watch?v=...
- Shorts: youtube.com/shorts/...
- Playlists: youtube.com/playlist?list=...

### VK
- Videos: vk.com/video-XXXXXX_XXXXXX
- Clips: vk.com/clip-XXXXXX_XXXXXX
- Alternative: vkvideo.ru/...

## Settings

- **Auto-open folder**: Opens downloads folder after completion
- **Change folder**: Select where to save downloads
- **Language selection**: Choose video language when available
- **Format selection**: Different qualities up to 4K

## Troubleshooting

### Common Issues
1. **Download fails**:
   - Check your internet connection
   - Try updating yt-dlp: run setup.bat
   - Check logs folder for details

2. **No video formats available**:
   - Click "Get Info" again
   - Check if the video is available in your region
   - Try another video to verify the program works

3. **SSL Certificate errors**:
   - Run setup.bat to update components
   - Check if your antivirus is blocking connections

4. **FFmpeg errors**:
   - Run setup.bat to download latest ffmpeg
   - Check if ffmpeg.exe exists in program folder

### Log Files
- Check logs folder for detailed error information
- Include log files when reporting issues

## Updates

- The program checks for yt-dlp updates during setup
- Manual update: run setup.bat
- Check [Releases](link_to_releases) for program updates

## Support

- Issues: Use GitHub Issues
- Questions: Telegram [@JL_Stable_Diffusion](https://t.me/JL_Stable_Diffusion)