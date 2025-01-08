# Contributing Guide

## How to Contribute

1. Fork the repository
2. Create a branch for the new feature or fix
3. Make changes following the code standards
4. Create a pull request with a description of changes

## Code Standards

- Use Python 3.10 or newer
- Follow PEP 8
- Add types for new functions
- Update documentation when needed

## Project Structure

```
jl-youtube-vk-downloader/
├── src/
│   ├── assets/
│   │   └── icon.ico
│   ├── downloader.py
│   ├── gui.py
│   └── main.py
├── docs/
│   ├── en/
│   │   ├── CHANGELOG.md
│   │   ├── CONTRIBUTING.md
│   │   └── GUIDE.md
│   └── ru/
│       ├── CHANGELOG.md
│       ├── CONTRIBUTING.md
│       └── GUIDE.md
├── .gitignore
├── build.bat
├── run.bat
├── setup.bat
└── requirements.txt
```

## Building the Project

1. Install dependencies:
```bash
setup.bat
```

2. Run for testing:
```bash
run.bat
```

3. Build exe file:
```bash
build.bat
```

## Testing

Test these operation modes:
- Single video download
- Multiple video download
- Playlist download
- Download in different formats
- MP3 conversion
- Auto-open folder
- Load/save URL lists
- Check all interface elements
- Check progress display

## Creating a Release

1. Update version in files
2. Update CHANGELOG.md
3. Build new exe version
4. Create new release on GitHub
5. Add change description

## Reporting Issues

- Use GitHub Issues section
- Specify program version
- Describe steps to reproduce the error
- Attach error log from logs folder